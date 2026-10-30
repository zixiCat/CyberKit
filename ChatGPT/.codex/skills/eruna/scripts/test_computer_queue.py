"""Exercise queue invariants using separate CLI processes; never touches the UI."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).with_name("computer_queue.py")


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="eruna-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.state = self.root / "state"
        self.call("init", "--executor", "desktop-executor", "--host", "test-host")

    def call(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(SCRIPT), "--state-dir", str(self.state), *args],
                                capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0 if ok else 1, result.stdout + result.stderr)
        return json.loads(result.stdout if ok else result.stderr)

    def request(self, job_id, requester="project-a", **changes):
        payload = {"id": job_id, "requester": {"threadId": requester, "hostId": "test-host"},
                   "objective": "Read a display", "target_app": "Test fixture (no real UI)",
                   "context": "Isolated queue test", "allowed_actions": ["Observe"],
                   "success_condition": "Return observed value", "authorization": "Test only; no UI authorized"}
        payload.update(changes)
        path = self.root / (job_id + "-" + requester + ".json")
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def submit(self, path):
        return self.call("submit", "--request", str(path))

    def claim(self):
        return self.call("claim", "--executor", "desktop-executor", "--host", "test-host")

    def finish(self, claim, status="completed", **changes):
        result = {"actual_actions": ["Observed test fixture"], "verified_outcome": "Fixture value: 0",
                  "evidence": ["Synthetic test fixture; not a desktop observation"], "blocker": ""}
        result.update(changes)
        path = self.root / "result.json"
        path.write_text(json.dumps(result), encoding="utf-8")
        return self.call("finish", "--id", claim["job"]["id"], "--token", claim["token"],
                         "--status", status, "--result", str(path))

    def test_concurrent_submissions_claims_fifo_and_release(self):
        paths = [self.request(f"job-{i}", requester=f"project-{i}") for i in range(12)]
        with ThreadPoolExecutor(max_workers=12) as pool:
            submitted = list(pool.map(self.submit, paths))
        expected = [r["job"]["id"] for r in sorted(submitted, key=lambda r: r["job"]["seq"])]
        self.assertEqual(len(set(expected)), 12)
        observed = []
        for job_id in expected:
            with ThreadPoolExecutor(max_workers=8) as pool:
                claims = list(pool.map(lambda _: self.claim(), range(8)))
            winners = [c for c in claims if c["claimed"]]
            self.assertEqual(len(winners), 1)
            self.assertTrue(all(c.get("reason") == "busy" for c in claims if not c["claimed"]))
            self.assertEqual(winners[0]["job"]["id"], job_id)
            observed.append(job_id)
            self.finish(winners[0])
        self.assertEqual(observed, expected)
        self.assertEqual(self.claim(), {"claimed": False, "reason": "empty"})
        self.assertIsNone(self.call("status")["owner"])

    def test_concurrent_dedupe_and_terminal_retry(self):
        path = self.request("same-attempt")
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(self.submit, [path] * 8))
        self.assertEqual(sum(not r["duplicate"] for r in results), 1)
        self.assertEqual(self.call("status")["counts"], {"queued": 1})
        self.finish(self.claim())
        duplicate = self.submit(path)
        self.assertTrue(duplicate["duplicate"])
        self.assertEqual(duplicate["job"]["status"], "completed")
        self.assertFalse(self.call("wake", "--id", "same-attempt")["should_send"])
        changed = self.request("same-attempt", objective="Different action")
        self.call("submit", "--request", str(changed), ok=False)

    def test_interrupted_owner_persists_and_never_replays(self):
        self.submit(self.request("first"))
        self.submit(self.request("second", requester="project-b"))
        claim = self.claim()
        self.call("interrupt", "--id", "first", "--note", "Simulated executor crash")
        self.assertEqual(self.claim()["reason"], "interrupted")
        self.call("recover", "--id", "first", "--note", "No stopped-input assertion", ok=False)
        self.call("cancel", "--id", "first", "--note", "Cannot cancel owner", ok=False)
        path = self.root / "result.json"
        path.write_text("{}", encoding="utf-8")
        self.call("finish", "--id", "first", "--token", claim["token"], "--status", "completed",
                  "--result", str(path), ok=False)
        recovered = self.call("recover", "--id", "first", "--confirm-stopped", "--note",
                              "Isolated fixture: no UI calls exist; old process has exited")
        self.assertEqual(recovered["status"], "failed")
        second = self.claim()
        self.assertEqual(second["job"]["id"], "second")
        self.call("finish", "--id", "second", "--token", claim["token"], "--status", "completed",
                  "--result", str(path), ok=False)
        self.finish(second)
        self.assertEqual(self.claim()["reason"], "empty")

    def test_token_fencing_result_persistence_and_no_token_leak(self):
        self.submit(self.request("fenced"))
        claim = self.claim()
        result_file = self.root / "unused.json"
        self.call("finish", "--id", "fenced", "--token", "wrong", "--status", "completed",
                  "--result", str(result_file), ok=False)
        self.assertEqual(self.claim()["reason"], "busy")
        self.assertNotIn("token", self.call("get", "--id", "fenced"))
        self.assertNotIn("token", self.call("status")["owner"])
        finished = self.finish(claim)
        self.assertEqual(self.call("get", "--id", "fenced"), finished)
        self.assertEqual(finished["result"]["verified_outcome"], "Fixture value: 0")

    def test_binding_and_payload_validation(self):
        self.call("init", "--executor", "different", "--host", "test-host", ok=False)
        self.call("claim", "--executor", "project-a", "--host", "test-host", ok=False)
        bad = self.request("invalid", allowed_actions=[])
        self.call("submit", "--request", str(bad), ok=False)
        remote = self.request("remote")
        payload = json.loads(remote.read_text(encoding="utf-8"))
        payload["requester"]["hostId"] = "other-host"
        remote.write_text(json.dumps(payload), encoding="utf-8")
        self.call("submit", "--request", str(remote), ok=False)
        self.assertEqual(self.call("status")["counts"], {})

    def test_supported_dispatch_arguments_apply_eruna_preference(self):
        self.submit(self.request("wake-job"))
        wake = self.call("wake", "--id", "wake-job")
        self.assertTrue(wake["should_send"])
        self.assertEqual(set(wake["arguments"]), {"threadId", "hostId", "prompt", "model", "thinking"})
        self.assertEqual(wake["arguments"]["threadId"], "desktop-executor")
        self.assertEqual(wake["arguments"]["model"], "gpt-6.1-terra")
        self.assertEqual(wake["arguments"]["thinking"], "medium")
        self.assertEqual(self.call("wake", "--id", "wake-job"), wake)
        self.assertEqual(self.call("get", "--id", "wake-job")["status"], "queued")

    def test_blocked_release_and_queued_cancel(self):
        self.submit(self.request("blocked"))
        self.submit(self.request("cancelled"))
        claim = self.claim()
        self.call("cancel", "--id", "cancelled", "--note", "Request withdrawn")
        self.finish(claim, status="blocked", actual_actions=[], evidence=[], blocker="Test prerequisite missing")
        self.assertEqual(self.claim()["reason"], "empty")

    def test_unverified_completion_does_not_release_owner(self):
        self.submit(self.request("unverified"))
        claim = self.claim()
        path = self.root / "unverified-result.json"
        path.write_text(json.dumps({"actual_actions": [], "verified_outcome": "Unknown",
                                    "evidence": [], "blocker": ""}), encoding="utf-8")
        self.call("finish", "--id", "unverified", "--token", claim["token"], "--status", "completed",
                  "--result", str(path), ok=False)
        self.assertEqual(self.claim()["reason"], "busy")
        self.finish(claim)

    def test_runtime_rejected_in_git_or_skill(self):
        from computer_queue import Queue
        checkout = self.root / "checkout"
        checkout.mkdir()
        (checkout / ".git").write_text("gitdir: fixture", encoding="utf-8")
        with self.assertRaises(ValueError):
            Queue(checkout / "private")
        skill = self.root / "skill"
        skill.mkdir()
        (skill / "SKILL.md").write_text("fixture", encoding="utf-8")
        with self.assertRaises(ValueError):
            Queue(skill / "state")


class DefaultStateTests(unittest.TestCase):
    def test_default_and_legacy_queue_preservation(self):
        from unittest.mock import patch
        from computer_queue import default_state_dir
        with tempfile.TemporaryDirectory(prefix="eruna-default-") as directory:
            root = Path(directory)
            with patch.dict("os.environ", {"CODEX_HOME": directory}):
                self.assertEqual(default_state_dir(), root / "eruna")
                legacy = root / "computer-task"
                legacy.mkdir()
                (legacy / "queue.sqlite3").touch()
                self.assertEqual(default_state_dir(), legacy)
                current = root / "eruna"
                current.mkdir()
                (current / "queue.sqlite3").touch()
                with self.assertRaises(ValueError):
                    default_state_dir()


if __name__ == "__main__":
    unittest.main()
