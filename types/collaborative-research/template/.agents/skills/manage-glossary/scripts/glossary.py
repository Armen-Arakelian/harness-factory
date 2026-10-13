#!/usr/bin/env python3
"""Manage one optional, link-free project glossary; never edit research notes."""
import argparse
from contextlib import contextmanager
import html
import json
import os
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parents[4]
FILE = ROOT / "glossary.md"


def clean(value):
    if not isinstance(value, str) or not value.strip() or "\n" in value or "\r" in value:
        raise ValueError("values must be nonempty single-line strings")
    if "[[" in value or "](" in value or re.search(r"https?://", value):
        raise ValueError("glossary entries must not contain links")
    return value.strip()


def normalize(value):
    return unicodedata.normalize("NFKC", value).strip().casefold()


def key(entry, languages):
    return normalize(entry["terms"][languages[0]]), normalize(entry.get("context", ""))


def validate(entry, languages):
    if not isinstance(entry, dict) or set(entry) - {"terms", "meaning", "context"}:
        raise ValueError("entry requires terms, meaning and optional context")
    if not isinstance(entry.get("terms"), dict) or set(entry["terms"]) != set(languages):
        raise ValueError("provide exactly the configured term languages")
    return {"terms": {language: clean(entry["terms"][language]) for language in languages},
            "context": clean(entry["context"]) if entry.get("context") else "",
            "meaning": clean(entry.get("meaning"))}


def read():
    if not FILE.exists():
        return None, None, []
    original = FILE.read_bytes()
    text = original.decode("utf-8")
    pieces = text.split("---\n", 2)
    if len(pieces) != 3 or pieces[0]:
        raise ValueError("glossary configuration is missing or malformed")
    config = {}
    for line in pieces[1].strip().splitlines():
        name, value = line.split(":", 1)
        config[name.strip()] = json.loads(value.strip())
    if set(config) != {"glossary_languages", "glossary_explanation_language", "glossary_enabled"}:
        raise ValueError("unexpected glossary configuration")
    languages = config["glossary_languages"]
    if not isinstance(languages, list) or not languages or any(not isinstance(x, str) for x in languages):
        raise ValueError("invalid languages")
    if len({normalize(x) for x in languages}) != len(languages) or any(clean(x) != x for x in languages):
        raise ValueError("invalid or duplicate languages")
    clean(config["glossary_explanation_language"])
    if not isinstance(config["glossary_enabled"], bool):
        raise ValueError("invalid enabled flag")
    rows = [line for line in pieces[2].splitlines() if line.startswith("|")]
    cells = lambda line: [html.unescape(x.strip()) for x in line.strip().strip("|").split("|")]
    if len(rows) < 2 or cells(rows[0]) != languages + ["Context", "Meaning"]:
        raise ValueError("glossary table does not match its configuration")
    if any(not re.fullmatch(r":?-{3,}:?", x) for x in cells(rows[1])) or len(cells(rows[1])) != len(languages) + 2:
        raise ValueError("malformed glossary table separator")
    entries, seen = [], set()
    for row in rows[2:]:
        values = cells(row)
        if len(values) != len(languages) + 2:
            raise ValueError("malformed glossary row")
        entry = validate({"terms": dict(zip(languages, values)), "context": values[-2], "meaning": values[-1]}, languages)
        identity = key(entry, languages)
        if identity in seen:
            raise ValueError("duplicate glossary row; reconcile explicitly")
        seen.add(identity); entries.append(entry)
    return original, config, entries


def write(original, config, entries):
    current = FILE.read_bytes() if FILE.exists() else None
    if current != original:
        raise ValueError("glossary changed; reread before retrying")
    languages = config["glossary_languages"]
    escape = lambda value: html.escape(value, quote=False).replace("|", "&#124;")
    lines = ["---"] + [name + ": " + json.dumps(value, ensure_ascii=False) for name, value in config.items()]
    lines += ["---", "# Glossary", "", "Agent-maintained terminology. Definitions are scoped aids, not user conclusions.", "",
              "| " + " | ".join(map(escape, languages + ["Context", "Meaning"])) + " |",
              "| " + " | ".join(["---"] * (len(languages) + 2)) + " |"]
    for entry in entries:
        values = [entry["terms"][language] for language in languages] + [entry["context"], entry["meaning"]]
        lines.append("| " + " | ".join(map(escape, values)) + " |")
    encoded = ("\n".join(lines) + "\n").encode("utf-8")
    if encoded == original:
        return False
    temp = FILE.with_suffix(".md.tmp")
    temp.write_bytes(encoded)
    if (FILE.read_bytes() if FILE.exists() else None) != original:
        temp.unlink(); raise ValueError("glossary changed before write")
    os.replace(temp, FILE)
    return True


@contextmanager
def lock():
    folder = ROOT / "work"; folder.mkdir(exist_ok=True)
    path = folder / "glossary.lock"
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError("glossary busy; retry later, do not bypass")
    try:
        os.close(fd); yield
    finally:
        path.unlink()


def execute(args):
    if args.command in {"config", "lookup"}:
        _, config, entries = read()
        if not config or not config["glossary_enabled"]:
            return {"enabled": False, "entries": []}
        if args.command == "config":
            return {"enabled": True, **config}
        queries = {normalize(x) for x in args.terms}
        return {"enabled": True, "entries": [e for e in entries if any(normalize(v) in queries for v in e["terms"].values())]}
    with lock():
        original, config, entries = read()
        if args.command == "create":
            if original is not None:
                raise ValueError("glossary already exists; preserve it")
            languages = [clean(value) for value in args.languages]
            if len({normalize(x) for x in languages}) != len(languages):
                raise ValueError("duplicate languages")
            config = {"glossary_languages": languages,
                      "glossary_explanation_language": clean(args.explanation_language), "glossary_enabled": True}
            write(None, config, [])
            return {"status": "created", **config}
        if not config:
            raise ValueError("glossary not created; no automatic opt-in")
        if args.command in {"disable", "enable"}:
            config["glossary_enabled"] = args.command == "enable"
            write(original, config, entries)
            return {"status": "enabled" if config["glossary_enabled"] else "disabled"}
        if not config["glossary_enabled"]:
            return {"status": "disabled", "changed": False}
        for name in args.sources:
            relative = Path(name)
            source = ROOT / relative
            if relative.is_absolute() or ".." in relative.parts or len(relative.parts) != 2 or relative.parts[0] not in {"nodes", "details"} or relative.suffix != ".md":
                raise ValueError("sources must be saved nodes/ or details/ notes")
            if not source.is_file() or source.is_symlink() or ROOT not in source.resolve().parents:
                raise ValueError("source missing or outside project")
        payload = json.loads(Path(args.entries).read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or set(payload) - {"entries", "remove"} or not isinstance(payload.get("entries"), list) or not isinstance(payload.get("remove", []), list):
            raise ValueError("payload requires entries list and optional remove list")
        removals = payload.get("remove", [])
        if removals and not args.review:
            raise ValueError("removal requires explicitly requested full review")
        languages = config["glossary_languages"]
        mapping = {key(e, languages): e for e in entries}
        for item in removals:
            if not isinstance(item, dict) or set(item) - {"term", "context"}:
                raise ValueError("removal requires term and optional context")
            identity = normalize(clean(item.get("term"))), normalize(item.get("context", ""))
            if identity not in mapping:
                raise ValueError("removal target not found")
            del mapping[identity]
        supplied = set()
        for item in payload["entries"]:
            entry = validate(item, languages); identity = key(entry, languages)
            if identity in supplied:
                raise ValueError("duplicate incoming term/context")
            supplied.add(identity); mapping[identity] = entry
        changed = write(original, config, list(mapping.values()))
        return {"status": "updated" if changed else "unchanged", "changed": changed, "term_count": len(mapping)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("config")
    create = sub.add_parser("create"); create.add_argument("--languages", nargs="+", required=True)
    create.add_argument("--explanation-language", required=True)
    lookup = sub.add_parser("lookup"); lookup.add_argument("--terms", nargs="+", required=True)
    sub.add_parser("disable"); sub.add_parser("enable")
    merge = sub.add_parser("merge"); merge.add_argument("--entries", required=True)
    merge.add_argument("--sources", nargs="+", required=True); merge.add_argument("--review", action="store_true")
    try:
        result = execute(parser.parse_args())
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        print(json.dumps({"status": "error", "reason": str(error)})); return 1
    print(json.dumps(result, ensure_ascii=False)); return 0


if __name__ == "__main__":
    sys.exit(main())
