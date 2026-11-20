"""Real helper subprocesses against disposable generated projects."""
import concurrent.futures
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import uuid

ROOT = Path(__file__).resolve().parents[1]


class ConcurrentApprovalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="approval-chats-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "research"
        subprocess.run([sys.executable, str(ROOT / "scripts/init.py"), "--type", "collaborative-research",
                        "--name", "Concurrency", "--topic", "Fixtures", "--destination", str(self.project)],
                       check=True, capture_output=True)
        self.helper = self.project / ".agents/skills/memory-approval/scripts/approval.py"

    def call(self, session, *args, ok=True):
        result = subprocess.run([sys.executable, str(self.helper), *args, "--session", session], capture_output=True, text=True)
        self.assertEqual(result.returncode == 0, ok, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def json_file(self, value):
        path = Path(self.temp.name) / (uuid.uuid4().hex + ".json")
        path.write_text(json.dumps(value))
        return str(path)

    def proposal(self, session, target="conclusions/example.md", kind="conclusion", action="create"):
        basis = self.call(session, "snapshot", "--paths", target)
        preview = {"kind": kind, "title": "Example", "changes": [{"path": target, "action": action, "text": "Exact thought."}]}
        return self.call(session, "create", "--preview", self.json_file(preview), "--basis", self.json_file(basis))["id"]

    def manifest(self, session, paths):
        snapshot = self.call(session, "snapshot", "--paths", *paths)
        return {"writes": [{"path": f["path"], "expected_sha256": f["sha256"],
                            "text": (f["text"] or "") + "Exact thought.\n"} for f in snapshot["files"]]}

    def test_independent_chats_and_scoped_expiry(self):
        a = self.proposal("A", "research-topics.md", "topics", "edit")
        b = self.proposal("B")
        self.call("C", "expire")  # opening another chat is harmless
        self.call("A", "approve", "--id", b, ok=False)
        self.call("B", "expire")
        self.call("B", "approve", "--id", b, ok=False)
        self.call("A", "approve", "--id", a)

    def test_supersession_is_local(self):
        a = self.proposal("A")
        b = self.proposal("B", "conclusions/b.md")
        newer = self.proposal("A", "conclusions/newer.md")
        self.call("A", "approve", "--id", a, ok=False)
        self.call("A", "cancel", "--id", newer)
        self.call("B", "approve", "--id", b)

    def test_no_time_deadline_and_single_use(self):
        a = self.proposal("A")
        registry = self.project / "work/memory-approvals.json"
        data = json.loads(registry.read_text())
        data["records"][a]["created_at"] = "2000-01-01T00:00:00+00:00"
        registry.write_text(json.dumps(data))
        self.call("A", "approve", "--id", a)
        self.call("A", "approve", "--id", a, ok=False)
        manifest = self.manifest("A", ["conclusions/example.md"])
        self.call("A", "apply", "--id", a, "--manifest", self.json_file(manifest))
        self.call("A", "apply", "--id", a, "--manifest", self.json_file(manifest), ok=False)

    def test_changes_before_and_after_approval_reject_without_writes(self):
        a = self.proposal("A")
        target = self.project / "conclusions/example.md"
        target.write_text("Other chat's content")
        self.call("A", "approve", "--id", a, ok=False)
        target.unlink()
        self.call("A", "approve", "--id", a)
        manifest = self.manifest("A", ["conclusions/example.md", "README.md"])
        target.write_text("Other chat's content")
        before = (self.project / "README.md").read_bytes()
        self.call("A", "apply", "--id", a, "--manifest", self.json_file(manifest), ok=False)
        self.assertEqual(target.read_text(), "Other chat's content")
        self.assertEqual((self.project / "README.md").read_bytes(), before)

    def test_shared_readme_conflict_can_be_rebuilt(self):
        a = self.proposal("A", "conclusions/a.md")
        b = self.proposal("B", "conclusions/b.md")
        self.call("A", "approve", "--id", a)
        self.call("B", "approve", "--id", b)
        ma = self.manifest("A", ["conclusions/a.md", "README.md"])
        mb = self.manifest("B", ["conclusions/b.md", "README.md"])
        self.call("A", "apply", "--id", a, "--manifest", self.json_file(ma))
        self.call("B", "apply", "--id", b, "--manifest", self.json_file(mb), ok=False)
        self.assertFalse((self.project / "conclusions/b.md").exists())
        mb = self.manifest("B", ["conclusions/b.md", "README.md"])
        self.call("B", "apply", "--id", b, "--manifest", self.json_file(mb))
        self.assertTrue((self.project / "README.md").read_text().endswith("Exact thought.\nExact thought.\n"))

    def test_preparing_preview_uses_original_snapshot(self):
        basis = self.call("A", "snapshot", "--paths", "research-topics.md")
        (self.project / "research-topics.md").write_text("Changed")
        preview = {"kind": "topics", "title": "Topics", "changes": [{"path": "research-topics.md", "action": "edit", "text": "New topics"}]}
        self.call("A", "create", "--preview", self.json_file(preview), "--basis", self.json_file(basis), ok=False)

    def test_legacy_registry_and_missing_session_fail_closed(self):
        registry = self.project / "work/memory-approvals.json"
        registry.write_text(json.dumps({"version": 1, "id": "old", "status": "pending"}))
        self.call("A", "approve", "--id", "old", ok=False)
        a = self.proposal("A")
        self.assertIn("legacy", json.loads(registry.read_text()))
        result = subprocess.run([sys.executable, str(self.helper), "expire"], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.call("A", "approve", "--id", a)

    def test_symlink_and_unapproved_paths_rejected(self):
        outside = Path(self.temp.name) / "outside.md"
        outside.write_text("untouched")
        (self.project / "nodes/link.md").symlink_to(outside)
        self.call("A", "snapshot", "--paths", "nodes/link.md", ok=False)
        a = self.proposal("A")
        self.call("A", "approve", "--id", a)
        manifest = self.manifest("A", ["conclusions/example.md"])
        manifest["writes"].append({"path": "rules.md", "expected_sha256": None, "text": "bad"})
        self.call("A", "apply", "--id", a, "--manifest", self.json_file(manifest), ok=False)
        self.assertFalse((self.project / "conclusions/example.md").exists())
        self.assertEqual(outside.read_text(), "untouched")

    def test_apply_complete_mixed_package_including_delete(self):
        (self.project / "nodes/edit.md").write_text("Old information")
        (self.project / "nodes/remove.md").write_text("Remove this")
        targets = ["nodes/new.md", "nodes/edit.md", "nodes/remove.md"]
        basis = self.call("A", "snapshot", "--paths", *targets)
        preview = {"kind": "batch", "title": "Mixed package", "changes": [
            {"path": name, "action": action, "text": text} for name, action, text in zip(
                targets, ["create", "edit", "delete"], ["New information", "Updated information", "Remove this"])]}
        a = self.call("A", "create", "--preview", self.json_file(preview), "--basis", self.json_file(basis))["id"]
        self.call("A", "approve", "--id", a)
        manifest = {"writes": [{"path": f["path"], "expected_sha256": f["sha256"], "text": text}
                               for f, text in zip(basis["files"], ["New information", "Updated information", None])]}
        incomplete = {"writes": manifest["writes"][:1]}
        self.call("A", "apply", "--id", a, "--manifest", self.json_file(incomplete), ok=False)
        self.assertFalse((self.project / "nodes/new.md").exists())
        self.call("A", "apply", "--id", a, "--manifest", self.json_file(manifest))
        self.assertEqual((self.project / "nodes/new.md").read_text(), "New information")
        self.assertEqual((self.project / "nodes/edit.md").read_text(), "Updated information")
        self.assertFalse((self.project / "nodes/remove.md").exists())

    def test_partial_failure_records_written_paths_and_cannot_replay(self):
        a = self.proposal("A")
        self.call("A", "approve", "--id", a)
        manifest = self.json_file(self.manifest("A", ["conclusions/example.md", "README.md"]))
        spec = importlib.util.spec_from_file_location("isolated_approval", self.helper)
        module = importlib.util.module_from_spec(spec)
        with patch.object(sys, "dont_write_bytecode", True):
            spec.loader.exec_module(module)
        replace = module.os.replace

        def fail_readme(source, target):
            if Path(target).resolve() == (self.project / "README.md").resolve():
                raise OSError("simulated write failure")
            return replace(source, target)

        with patch.object(module.os, "replace", side_effect=fail_readme):
            with self.assertRaises(OSError):
                from argparse import Namespace
                module.run(Namespace(command="apply", session="A", id=a, manifest=manifest))
        record = json.loads((self.project / "work/memory-approvals.json").read_text())["records"][a]
        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["written"], ["conclusions/example.md"])
        self.call("A", "apply", "--id", a, "--manifest", manifest, ok=False)

    def test_parallel_apply_has_one_winner_for_shared_file(self):
        tasks = []
        for session in ["A", "B"]:
            target = "conclusions/" + session + ".md"
            proposal = self.proposal(session, target)
            self.call(session, "approve", "--id", proposal)
            manifest = self.json_file(self.manifest(session, [target, "README.md"]))
            tasks.append([sys.executable, str(self.helper), "apply", "--session", session, "--id", proposal, "--manifest", manifest])
        with concurrent.futures.ThreadPoolExecutor() as pool:
            results = list(pool.map(lambda command: subprocess.run(command, capture_output=True), tasks))
        self.assertEqual(sorted(r.returncode for r in results), [0, 1])
        self.assertEqual(sum((self.project / ("conclusions/" + s + ".md")).exists() for s in ["A", "B"]), 1)


if __name__ == "__main__":
    unittest.main()
