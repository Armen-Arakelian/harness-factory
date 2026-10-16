#!/usr/bin/env python3
"""Create an independent project from a Harness Factory type (standard library only)."""

import argparse
import json
from pathlib import Path
import re
import sys


FACTORY_ROOT = Path(__file__).resolve().parents[1]
RESERVED_ARGUMENTS = {"type", "name", "destination", "list-types", "help"}


def nonempty(value):
    value = value.strip()
    if not value:
        raise argparse.ArgumentTypeError("value must not be empty")
    return value


def project_name(value):
    value = nonempty(value)
    if "\n" in value or "\r" in value:
        raise argparse.ArgumentTypeError("project name must be a single line")
    return value


def load_types():
    """Discover type-local descriptors without a central registry."""
    result = {}
    root = FACTORY_ROOT / "types"
    for folder in sorted(root.iterdir()):
        if not folder.is_dir() or folder.is_symlink() or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", folder.name):
            continue
        descriptor = folder / "project.json"
        if not descriptor.is_file():
            continue
        if descriptor.is_symlink():
            raise ValueError(f"type descriptor symlinks are unsupported: {descriptor}")
        data = json.loads(descriptor.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError(f"invalid type descriptor: {descriptor}")
        for key in ("display_name", "description"):
            if not isinstance(data.get(key), str) or not data[key].strip():
                raise ValueError(f"missing {key}: {descriptor}")
        parameters = data.get("parameters")
        if not isinstance(parameters, dict):
            raise ValueError(f"parameters must be an object: {descriptor}")
        tokens = {"PROJECT_NAME"}
        for name, spec in parameters.items():
            if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", name) or name in RESERVED_ARGUMENTS:
                raise ValueError(f"invalid or reserved parameter {name}: {descriptor}")
            if not isinstance(spec, dict) or not isinstance(spec.get("help"), str) or not spec["help"].strip():
                raise ValueError(f"parameter {name} requires help text: {descriptor}")
            token = spec.get("token")
            if not isinstance(token, str) or not re.fullmatch(r"[A-Z][A-Z0-9_]*", token) or token in tokens:
                raise ValueError(f"invalid or duplicate token for {name}: {descriptor}")
            tokens.add(token)
        result[folder.name] = data
    if not result:
        raise ValueError("no supported project types found")
    return result


def generate(type_id, replacements, destination):
    """Read the complete blueprint before exclusively creating its destination."""
    template_root = FACTORY_ROOT / "types" / type_id / "template"
    if not template_root.is_dir() or template_root.is_symlink():
        raise ValueError(f"missing or unsupported template directory: {template_root}")
    resolved = destination.resolve()
    if resolved == FACTORY_ROOT or FACTORY_ROOT in resolved.parents:
        raise ValueError("destination must be outside Harness Factory")
    files, directories = {}, []
    pattern = re.compile("|".join(re.escape(token) for token in replacements))
    for source in sorted(template_root.rglob("*")):
        if source.name == ".DS_Store":
            continue
        if source.is_symlink():
            raise ValueError(f"template symlinks are unsupported: {source}")
        relative = source.relative_to(template_root)
        if source.is_dir():
            directories.append(relative)
        elif source.is_file():
            content = source.read_text(encoding="utf-8")
            if source.suffix == ".md":
                # One pass keeps user-supplied template-like text literal.
                content = pattern.sub(lambda match: replacements[match.group(0)], content)
            files[relative] = content
    if not files:
        raise ValueError("project template contains no files")
    destination.mkdir(parents=True, exist_ok=False)
    for relative in directories:
        (destination / relative).mkdir(parents=True, exist_ok=True)
    for relative, content in files.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8", newline="\n") as output:
            output.write(content)


def main():
    try:
        project_types = load_types()
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    selector = argparse.ArgumentParser(add_help=False)
    selector.add_argument("--type", choices=project_types)
    selector.add_argument("--list-types", action="store_true")
    selected, _ = selector.parse_known_args()
    if selected.list_types:
        for type_id, info in project_types.items():
            print(f"{type_id}: {info['display_name']} — {info['description']}")
        return 0

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--type", choices=project_types, required=True, help="Project type")
    parser.add_argument("--list-types", action="store_true", help="List available project types")
    parser.add_argument("--name", required=True, type=project_name, help="Project title")
    parser.add_argument("--destination", required=True, type=nonempty, help="New folder outside the factory; must not exist")
    parameters = project_types[selected.type]["parameters"] if selected.type else {}
    for name, spec in parameters.items():
        parser.add_argument(f"--{name}", required=True, type=nonempty, help=spec["help"])
    args = parser.parse_args()
    destination = Path(args.destination).expanduser().absolute()
    replacements = {"{{PROJECT_NAME}}": args.name}
    for name, spec in parameters.items():
        replacements["{{" + spec["token"] + "}}"] = getattr(args, name.replace("-", "_"))
    try:
        generate(args.type, replacements, destination)
    except FileExistsError:
        print(f"Error: destination or output file already exists: {destination}", file=sys.stderr)
        return 1
    except (OSError, ValueError) as error:
        print(f"Error: {error}. Check destination for partial output: {destination}", file=sys.stderr)
        return 1
    print(f"Created {project_types[args.type]['display_name']} project: {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
