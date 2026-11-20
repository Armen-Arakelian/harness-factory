#!/usr/bin/env python3
"""Local, one-use approval registry. Validates previews and serializes approved memory writes."""
import argparse
from contextlib import contextmanager
import hashlib
import json
import os
import re
from pathlib import Path
import sys
import uuid
from datetime import datetime, timezone
import tempfile

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
        return {"version": 2, "records": {}}
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if not isinstance(registry, dict):
        raise ValueError("invalid registry")
    if registry.get("version") == 1:
        # Old records have no chat owner or file baseline. Preserve for diagnosis,
        # but never accept them under the new protocol.
        return {"version": 2, "records": {}, "legacy": registry}
    if registry.get("version") != 2 or not isinstance(registry.get("records"), dict):
        raise ValueError("invalid registry")
    return registry


def destination(name):
    if not isinstance(name, str) or "\\" in name:
        raise ValueError("invalid destination")
    path = Path(name)
    allowed = name in {"README.md", "research-topics.md", "ideas.md"} or (
        len(path.parts) == 2 and path.parts[0] in {"nodes", "people", "conclusions", "details"}
        and path.suffix == ".md")
    if not allowed or path.is_absolute() or ".." in path.parts or path.as_posix() != name:
        raise ValueError("invalid curated destination")
    target = ROOT / path
    if any((ROOT / Path(*path.parts[:i])).is_symlink() for i in range(1, len(path.parts) + 1)):
        raise ValueError("symlink destination rejected")
    return target


def file_hash(name):
    path = destination(name)
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def unchanged(record):
    for name, expected in record["basis"].items():
        if file_hash(name) != expected:
            raise ValueError("target changed; fresh preview required: " + name)


def apply(registry, record, manifest_path):
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or set(manifest) != {"writes"} or not isinstance(manifest["writes"], list):
        raise ValueError("manifest requires writes")
    writes = {}
    for item in manifest["writes"]:
        if not isinstance(item, dict) or set(item) != {"path", "expected_sha256", "text"}:
            raise ValueError("write requires path, expected_sha256 and text (null for delete)")
        name = item["path"]
        destination(name)
        if name in writes or (item["text"] is not None and not isinstance(item["text"], str)):
            raise ValueError("duplicate path or invalid text")
        expected = item["expected_sha256"]
        if expected is not None and (not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected)):
            raise ValueError("invalid expected_sha256")
        if file_hash(name) != expected:
            raise ValueError("write conflict; reread files and rebuild manifest: " + name)
        writes[name] = item
    unchanged(record)
    for change in record["preview"]["changes"]:
        item = writes.get(change["path"])
        if item is None or (item["text"] is None) != (change["action"] == "delete"):
            raise ValueError("manifest must apply every approved change with its approved action")
    # Additional files may contain only delegated mechanical link/map edits.
    # The agent checks meaning and exact preview fidelity; hashes cannot do that.
    record["status"] = "applying"
    record["written"] = []
    write(registry)
    try:
        for name, item in writes.items():
            target = destination(name)
            if item["text"] is None:
                target.unlink()
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                fd, temporary = tempfile.mkstemp(prefix=".memory-", dir=target.parent)
                try:
                    with os.fdopen(fd, "w", encoding="utf-8", newline="") as output:
                        output.write(item["text"])
                    os.replace(temporary, target)
                finally:
                    if os.path.exists(temporary):
                        os.unlink(temporary)
            record["written"].append(name)
            write(registry)
    except OSError:
        record["status"] = "failed"
        write(registry)
        raise
    record["status"] = "applied"
    write(registry)
    return {"status": "saved", "id": record["id"], "written": record["written"]}


def write(record):
    temp = REGISTRY.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as output:
        json.dump(record, output, ensure_ascii=False, indent=2)
        output.write("\n")
    os.replace(temp, REGISTRY)


def run(args):
    if not args.session or not re.fullmatch(r"[A-Za-z0-9_.:-]{1,160}", args.session):
        raise ValueError("provide a stable, chat-specific session ID")
    with locked():
        registry = read()
        records = registry["records"]
        if args.command == "snapshot":
            return {"files": [{"path": name, "sha256": file_hash(name),
                               "text": destination(name).read_text(encoding="utf-8")
                               if destination(name).exists() else None} for name in args.paths]}
        if args.command == "expire":
            expired = []
            for record in records.values():
                if record["session"] == args.session and record["status"] in {"pending", "consumed"}:
                    record["status"] = "expired"
                    expired.append(record["id"])
            write(registry)
            return {"status": "expired" if expired else "no-pending-preview", "ids": expired}
        if args.command == "create":
            preview = json.loads(Path(args.preview).read_text(encoding="utf-8"))
            validate(preview)
            snapshot = json.loads(Path(args.basis).read_text(encoding="utf-8"))
            basis = {item["path"]: item["sha256"] for item in snapshot["files"]}
            if set(basis) != {c["path"] for c in preview["changes"]}:
                raise ValueError("basis must contain exactly the preview targets")
            for name, expected in basis.items():
                if file_hash(name) != expected:
                    raise ValueError("target changed while preparing preview: " + name)
            for change in preview["changes"]:
                exists = basis[change["path"]] is not None
                if (change["action"] == "create") == exists:
                    raise ValueError("create needs an absent target; edit/delete need an existing target")
            for old in records.values():
                if old["session"] == args.session and old["status"] in {"pending", "consumed"}:
                    old["status"] = "superseded"
            record = {"id": uuid.uuid4().hex, "session": args.session, "status": "pending",
                      "created_at": datetime.now(timezone.utc).isoformat(),
                      "preview": preview, "hash": digest(preview), "basis": basis}
            records[record["id"]] = record
            write(registry)
            return {"status": "pending", "id": record["id"], "preview": preview}
        record = records.get(args.id)
        if not record or record.get("session") != args.session:
            raise ValueError("rejected: unknown ID or different chat")
        expected_status = "consumed" if args.command == "apply" else "pending"
        if record.get("status") != expected_status:
            raise ValueError("rejected: " + str(record.get("status", "invalid status")))
        validate(record["preview"])
        if record.get("hash") != digest(record["preview"]):
            raise ValueError("rejected: preview changed")
        if args.command == "apply":
            return apply(registry, record, args.manifest)
        if args.command == "render":
            data = {"id": record["id"], **record["preview"]}
            encoded = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
            fragment = ASSET.read_text(encoding="utf-8")
            fragment = fragment.replace("__APPROVAL_ROOT__", "memory-approval-" + record["id"])
            fragment = fragment.replace("__APPROVAL_DATA__", encoded)
            with Path(args.output).open("x", encoding="utf-8") as target:
                target.write(fragment)
            return {"status": "rendered", "path": str(Path(args.output).absolute())}
        if args.command == "approve":
            unchanged(record)
        record["status"] = "consumed" if args.command == "approve" else "cancelled"
        write(registry)
        result = {"status": "accepted" if args.command == "approve" else "cancelled", "id": record["id"]}
        if args.command == "approve":
            result.update(preview=record["preview"], basis=record["basis"])
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("expire", help="Expire only this chat on an ordinary turn")
    snapshot = commands.add_parser("snapshot", help="Read latest files and hashes for a write manifest")
    snapshot.add_argument("--paths", nargs="+", required=True)
    create = commands.add_parser("create")
    create.add_argument("--basis", required=True, help="Snapshot JSON read before preparing the preview")
    create.add_argument("--preview", required=True, help="JSON file with exact preview content")
    for name in ("approve", "cancel", "render", "apply"):
        command = commands.add_parser(name)
        command.add_argument("--id", required=True)
        if name == "render":
            command.add_argument("--output", required=True)
        if name == "apply":
            command.add_argument("--manifest", required=True)
    for command in commands.choices.values():
        command.add_argument("--session", required=True, help="Stable chat-specific ID; never a project-wide default")
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
