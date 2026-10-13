#!/usr/bin/env python3
"""Smoke-check selected Factory blueprints without network or Git mutations."""
import argparse
import importlib.util
from pathlib import Path
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[4]


def snapshot(root):
    directories, files = set(), {}
    for item in root.rglob("*"):
        if item.is_symlink():
            raise ValueError(f"generated symlink: {item}")
        relative = item.relative_to(root).as_posix()
        if item.is_dir():
            directories.add(relative)
        elif item.is_file():
            files[relative] = item.read_bytes()
    return directories, files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--type", action="append", dest="types", help="Type ID; repeat to select several. Default: all types.")
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("factory_generator", ROOT / "scripts/init.py")
    if spec is None or spec.loader is None:
        raise ValueError("cannot load Factory generator")
    generator = importlib.util.module_from_spec(spec)
    # Importing the generator must not leave caches in the source project.
    previous = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(generator)
    finally:
        sys.dont_write_bytecode = previous
    available = generator.load_types()
    selected = sorted(set(args.types or available))
    unknown = set(selected) - set(available)
    if unknown:
        raise ValueError("unknown types: " + ", ".join(sorted(unknown)))
    with tempfile.TemporaryDirectory(prefix="factory-check-") as folder:
        temporary = Path(folder)
        if temporary.resolve() == ROOT or ROOT in temporary.resolve().parents:
            raise ValueError("temporary directory must be outside Factory")
        for type_id in selected:
            replacements = {"{{PROJECT_NAME}}": "Factory Smoke Check"}
            for name, parameter in available[type_id]["parameters"].items():
                replacements["{{" + parameter["token"] + "}}"] = "Check value for " + name
            first, second = temporary / (type_id + "-first"), temporary / (type_id + "-second")
            generator.generate(type_id, replacements, first)
            generator.generate(type_id, replacements, second)
            first_snapshot = snapshot(first)
            if first_snapshot != snapshot(second):
                raise ValueError(f"non-deterministic output: {type_id}")
            for relative, content in first_snapshot[1].items():
                if relative.endswith(".md"):
                    text = content.decode("utf-8")
                    if any(token in text for token in replacements):
                        raise ValueError(f"unrendered placeholder: {type_id}/{relative}")
                if Path(relative).name == ".factory.local.json" or relative == "work/memory-approvals.json":
                    raise ValueError(f"local runtime/configuration in blueprint: {type_id}/{relative}")
            blueprint = ROOT / "types" / type_id / "template"
            expected_directories = set()
            expected_files = set()
            for source in blueprint.rglob("*"):
                if source.name == ".DS_Store":
                    continue
                relative = source.relative_to(blueprint).as_posix()
                if source.is_dir():
                    expected_directories.add(relative)
                elif source.is_file():
                    expected_files.add(relative)
                    if source.suffix != ".md" and source.read_bytes() != first_snapshot[1].get(relative):
                        raise ValueError(f"copied asset changed: {type_id}/{relative}")
            if expected_directories != first_snapshot[0] or expected_files != set(first_snapshot[1]):
                raise ValueError(f"missing or unexpected generated paths: {type_id}")
            # Reusing a destination must refuse, rather than overwrite, the project.
            before = snapshot(first)
            try:
                generator.generate(type_id, replacements, first)
            except FileExistsError:
                pass
            else:
                raise ValueError(f"existing destination was accepted: {type_id}")
            if snapshot(first) != before:
                raise ValueError(f"existing destination was modified: {type_id}")
            empty = temporary / (type_id + "-empty")
            empty.mkdir()
            try:
                generator.generate(type_id, replacements, empty)
            except FileExistsError:
                pass
            else:
                raise ValueError(f"existing empty destination was accepted: {type_id}")
            if snapshot(empty) != (set(), {}):
                raise ValueError(f"existing empty destination was modified: {type_id}")
            print(f"PASS: {type_id}: deterministic output, complete paths/assets, existing destinations preserved")
    print("Generation smoke checks passed. Workflow behavior and documentation still need scoped review.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
