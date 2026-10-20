#!/usr/bin/env python3
"""Local, one-use approval registry. Does not write curated research memory."""
import argparse
from contextlib import contextmanager
import hashlib
import json
import os
import re
from pathlib import Path
import sys
import uuid

ROOT = Path(__file__).resolve().parents[4]
REGISTRY = ROOT / "work" / "memory-approvals.json"
ASSET = Path(__file__).resolve().parents[1] / "assets" / "card.html"


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                    separators=(",", ":")).encode()).hexdigest()


def validate(preview):
    if not isinstance(preview, dict) or set(preview) != {"kind", "title", "changes"}:
        raise ValueError("preview requires only kind, title and changes")
    if preview["kind"] not in {"information", "conclusion", "details", "maintenance", "topics", "ideas", "person", "batch"}:
        raise ValueError("unsupported preview kind")
    if not isinstance(preview["title"], str) or not preview["title"].strip() or "\n" in preview["title"]:
        raise ValueError("title must be a nonempty single line")
    if not isinstance(preview["changes"], list) or not preview["changes"]:
        raise ValueError("changes must be a nonempty list")
    if preview["kind"] == "batch" and len(preview["changes"]) < 2:
        raise ValueError("batch preview requires at least two substantive changes")
    seen = set()
    for change in preview["changes"]:
        if not isinstance(change, dict) or set(change) != {"path", "action", "text"}:
            raise ValueError("each change requires only path, action and text")
        name = change["path"]
        if not isinstance(name, str) or "\\" in name:
            raise ValueError("use project-relative paths")
        path = Path(name)
        allowed = name in {"README.md", "research-topics.md", "ideas.md"} or (len(path.parts) == 2 and
                  path.parts[0] in {"nodes", "people", "conclusions", "details"} and path.suffix == ".md")
        if not allowed or path.is_absolute() or ".." in path.parts or name in seen:
            raise ValueError("invalid or duplicate curated destination")
        if (preview["kind"] == "topics") != (name == "research-topics.md"):
            raise ValueError("topics previews target only research-topics.md")
        if (preview["kind"] == "ideas") != (name == "ideas.md"):
            raise ValueError("ideas previews target only ideas.md")
        seen.add(name)
        if change["action"] not in {"create", "edit", "delete"}:
            raise ValueError("unsupported action; preview renames as deletion plus creation")
        if not isinstance(change["text"], str) or not change["text"].strip():
            raise ValueError("provide exact substantive text, or a deletion description")
        if path.parts[0] == "people":
            if preview["kind"] not in {"person", "maintenance", "batch"}:
                raise ValueError("people changes use person, batch or maintenance previews")
            if change["action"] != "delete":
                sections = change["text"].split("---\n", 2)
                if len(sections) != 3 or sections[0]:
                    raise ValueError("person preview requires contact-status frontmatter")
                statuses = [line for line in sections[1].splitlines() if line.startswith("contact_status:")]
                if len(statuses) != 1 or not re.fullmatch(r"contact_status: (contact|public-figure)", statuses[0]):
                    raise ValueError("person preview needs one canonical contact_status")
    if preview["kind"] == "person" and not any(Path(c["path"]).parts[0] == "people" for c in preview["changes"]):
        raise ValueError("person preview must include a people note")


@contextmanager
def locked():
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    lock = REGISTRY.with_suffix(".lock")
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError("registry busy; retry later, never bypass the check")
    try:
        os.close(fd)
        yield
    finally:
        lock.unlink()


def read():
    if not REGISTRY.exists():
        return None
    record = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if not isinstance(record, dict) or record.get("version") != 1:
        raise ValueError("invalid registry")
    return record


def write(record):
    temp = REGISTRY.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as output:
        json.dump(record, output, ensure_ascii=False, indent=2)
        output.write("\n")
    os.replace(temp, REGISTRY)


def run(args):
    with locked():
        record = read()
        if args.command == "expire":
            if record and record.get("status") == "pending":
                record["status"] = "expired"
                write(record)
                return {"status": "expired", "id": record["id"]}
            return {"status": "no-pending-preview"}
        if args.command == "create":
            preview = json.loads(Path(args.preview).read_text(encoding="utf-8"))
            validate(preview)
            record = {"version": 1, "id": uuid.uuid4().hex, "status": "pending",
                      "preview": preview, "hash": digest(preview)}
            write(record)
            return {"status": "pending", "id": record["id"], "preview": preview}
        if not record or record.get("id") != args.id:
            raise ValueError("rejected: unknown or superseded ID")
        if record.get("status") != "pending":
            raise ValueError("rejected: " + str(record.get("status", "invalid status")))
        validate(record["preview"])
        if record.get("hash") != digest(record["preview"]):
            raise ValueError("rejected: preview changed")
        if args.command == "render":
            data = {"id": record["id"], **record["preview"]}
            encoded = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
            fragment = ASSET.read_text(encoding="utf-8")
            fragment = fragment.replace("__APPROVAL_ROOT__", "memory-approval-" + record["id"])
            fragment = fragment.replace("__APPROVAL_DATA__", encoded)
            # Use only a host-approved visualization path supplied by the agent.
            output = Path(args.output)
            with output.open("x", encoding="utf-8") as target:
                target.write(fragment)
            return {"status": "rendered", "path": str(output.absolute())}
        record["status"] = "consumed" if args.command == "approve" else "cancelled"
        write(record)
        result = {"status": "accepted" if args.command == "approve" else "cancelled",
                  "id": record["id"]}
        if args.command == "approve":
            result["preview"] = record["preview"]
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("expire", help="Expire pending preview on an ordinary user turn")
    create = commands.add_parser("create")
    create.add_argument("--preview", required=True, help="JSON file with exact preview content")
    for name in ("approve", "cancel", "render"):
        command = commands.add_parser(name)
        command.add_argument("--id", required=True)
        if name == "render":
            command.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        result = run(args)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({"status": "rejected", "reason": str(error)}))
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
