"""Exercise ideas approval boundaries in disposable generated research projects."""
import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class IdeasApprovalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="factory-ideas-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / "research"
        subprocess.run([
            sys.executable, str(ROOT / "scripts/init.py"), "--type", "collaborative-research",
            "--name", "Ideas Check", "--destination", str(self.project), "--topic", "Fictional fixtures",
        ], check=True, capture_output=True)
        self.helper = self.project / ".agents/skills/memory-approval/scripts/approval.py"
        self.preview = {
            "kind": "ideas", "title": "Compare two approaches",
            "changes": [{"path": "ideas.md", "action": "edit", "text":
                "### Compare two approaches\n\n- **Status:** 💥 Cannon\n\nCompare their practical limits before choosing an approach."}],
        }

    def call(self, *args):
        return subprocess.run([sys.executable, str(self.helper), *args], capture_output=True, text=True)

    def register(self, preview=None, success=True):
        path = Path(self.temp.name) / "preview.json"
        path.write_text(json.dumps(preview or self.preview, ensure_ascii=False), encoding="utf-8")
        result = self.call("create", "--preview", str(path))
        self.assertEqual(result.returncode == 0, success, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_empty_list_generated_and_not_hidden(self):
        self.assertIn("No ideas saved yet.", (self.project / "ideas.md").read_text())
        graph = json.loads((self.project / ".obsidian/graph.json").read_text())
        group = next(g for g in graph["colorGroups"] if g["query"] == 'path:/^ideas\\.md$/')
        self.assertEqual(group["color"]["rgb"], 9133302)
        self.assertEqual(graph["search"], "")
        filters = json.loads((self.project / ".obsidian/app.json").read_text())["userIgnoreFilters"]
        self.assertFalse(any(re.search(pattern[1:-1], "ideas.md") for pattern in filters))
        self.assertTrue(any(re.search(pattern[1:-1], "details/example.md") for pattern in filters))

    def test_single_use_exact_approval_does_not_write_memory(self):
        before = (self.project / "ideas.md").read_bytes()
        pending = self.register()
        result = self.call("approve", "--id", pending["id"])
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)["preview"], self.preview)
        self.assertNotEqual(self.call("approve", "--id", pending["id"]).returncode, 0)
        self.assertEqual((self.project / "ideas.md").read_bytes(), before)

    def test_clarification_expires_preview(self):
        pending = self.register()
        self.assertEqual(self.call("expire").returncode, 0)
        self.assertNotEqual(self.call("approve", "--id", pending["id"]).returncode, 0)

    def test_cancel_and_supersede_reject_old_ids(self):
        first = self.register()
        second = self.register()
        self.assertNotEqual(self.call("approve", "--id", first["id"]).returncode, 0)
        self.assertEqual(self.call("cancel", "--id", second["id"]).returncode, 0)
        self.assertNotEqual(self.call("approve", "--id", second["id"]).returncode, 0)

    def test_tampering_is_rejected(self):
        pending = self.register()
        path = self.project / "work/memory-approvals.json"
        record = json.loads(path.read_text())
        record["preview"]["changes"][0]["text"] += " Unapproved change."
        path.write_text(json.dumps(record))
        self.assertNotEqual(self.call("approve", "--id", pending["id"]).returncode, 0)

    def test_ideas_kind_cannot_write_other_memory(self):
        for target in ["README.md", "research-topics.md", "nodes/example.md", "conclusions/example.md"]:
            with self.subTest(target=target):
                preview = copy.deepcopy(self.preview)
                preview["changes"][0]["path"] = target
                self.register(preview, success=False)

    def test_other_kinds_cannot_write_ideas(self):
        for kind in ["information", "conclusion", "details", "maintenance", "topics", "person"]:
            with self.subTest(kind=kind):
                preview = copy.deepcopy(self.preview)
                preview["kind"] = kind
                self.register(preview, success=False)

    def test_mixed_batch_does_not_silently_modify_ideas(self):
        preview = copy.deepcopy(self.preview)
        preview["kind"] = "batch"
        preview["changes"].append({"path": "nodes/example.md", "action": "create", "text": "Example fact."})
        self.register(preview, success=False)

    def test_invalid_and_duplicate_paths_rejected(self):
        for target in ["../ideas.md", "other/ideas.md", "/ideas.md", "ideas.md/extra"]:
            with self.subTest(target=target):
                preview = copy.deepcopy(self.preview)
                preview["changes"][0]["path"] = target
                self.register(preview, success=False)
        preview = copy.deepcopy(self.preview)
        preview["changes"].append(copy.deepcopy(preview["changes"][0]))
        self.register(preview, success=False)

    def test_multiple_entry_edits_use_one_file_and_id(self):
        preview = copy.deepcopy(self.preview)
        preview["changes"][0]["text"] += "\n\n### Another idea\n\n- **Status:** Tentative\n\nA separate possibility."
        pending = self.register(preview)
        accepted = json.loads(self.call("approve", "--id", pending["id"]).stdout)
        self.assertEqual(accepted["preview"], preview)
        self.assertEqual(len(accepted["preview"]["changes"]), 1)

    def test_existing_topics_and_note_batches_still_work(self):
        for preview in [
            {"kind": "topics", "title": "Question", "changes": [{"path": "research-topics.md", "action": "edit", "text": "An open question."}]},
            {"kind": "batch", "title": "Note with depth", "changes": [
                {"path": "nodes/example.md", "action": "create", "text": "Short explanation."},
                {"path": "details/example.md", "action": "create", "text": "Supporting detail."},
            ]},
        ]:
            with self.subTest(kind=preview["kind"]):
                pending = self.register(preview)
                self.assertEqual(self.call("approve", "--id", pending["id"]).returncode, 0)

    def test_render_escapes_untrusted_text_and_keeps_ideas_kind(self):
        preview = copy.deepcopy(self.preview)
        preview["changes"][0]["text"] += "\n</script><script>untrusted()</script>"
        pending = self.register(preview)
        path = Path(self.temp.name) / "card.html"
        result = self.call("render", "--id", pending["id"], "--output", str(path))
        self.assertEqual(result.returncode, 0, result.stdout)
        rendered = path.read_text()
        self.assertNotIn("</script><script>untrusted()", rendered)
        match = re.search(r"const preview = (.+);", rendered)
        self.assertIsNotNone(match)
        data = json.loads(match.group(1))
        self.assertEqual(data["kind"], "ideas")
        self.assertEqual(data["changes"], preview["changes"])
        self.assertEqual(data["id"], pending["id"])


if __name__ == "__main__":
    unittest.main()
