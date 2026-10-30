"""Cooperative single-desktop FIFO. Local SQLite only; never sends or performs UI."""
import argparse
import json
import os
from pathlib import Path
import secrets
import sqlite3
import sys
from datetime import datetime, timezone


def now():
    return datetime.now(timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def require_text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be nonempty text")


def text_list(value, name, nonempty=True):
    if not isinstance(value, list) or (nonempty and not value):
        raise ValueError(f"{name} must be a list" + (" with evidence/actions" if nonempty else ""))
    for item in value:
        require_text(item, name)


def read_json(path):
    value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError("JSON must be an object")
    return value


class Queue:
    def __init__(self, directory):
        directory = Path(directory).expanduser()
        if not directory.is_absolute():
            raise ValueError("state directory must be absolute")
        directory = directory.resolve()
        for parent in (directory, *directory.parents):
            if (parent / ".git").exists() or (parent / "SKILL.md").exists():
                raise ValueError("runtime state must be outside Git checkouts and skill folders")
        directory.mkdir(parents=True, exist_ok=True)
        self.directory = directory
        self.db = sqlite3.connect(directory / "queue.sqlite3", timeout=30, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS config (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS jobs (
                seq INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT UNIQUE NOT NULL,
                payload TEXT NOT NULL, status TEXT NOT NULL, token TEXT,
                created TEXT NOT NULL, updated TEXT NOT NULL, result TEXT, note TEXT);
            CREATE UNIQUE INDEX IF NOT EXISTS one_desktop_owner ON jobs ((1))
                WHERE status IN ('running', 'interrupted');
        """)

    def close(self):
        self.db.close()

    def binding(self):
        row = self.db.execute("SELECT value FROM config WHERE key='executor'").fetchone()
        if not row:
            raise ValueError("executor unbound; verify the existing chat and run init")
        return json.loads(row[0])

    def job(self, job_id):
        row = self.db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
        if not row:
            raise ValueError("unknown job ID")
        return row

    @staticmethod
    def public(row):
        return {k: json.loads(row[k]) if k in ("payload", "result") and row[k] else row[k]
                for k in row.keys() if k != "token"}

    def run(self, args):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            result = self.command(args)
            self.db.execute("COMMIT")
            return result
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

    def command(self, a):
        if a.command == "init":
            require_text(a.executor, "executor")
            require_text(a.host, "host")
            desired = {"threadId": a.executor, "hostId": a.host}
            row = self.db.execute("SELECT value FROM config WHERE key='executor'").fetchone()
            if row and json.loads(row[0]) != desired:
                raise ValueError("executor binding differs; preserve the existing queue and investigate")
            self.db.execute("INSERT OR IGNORE INTO config VALUES ('executor', ?)", (canonical(desired),))
            return {"executor": desired, "state_dir": str(self.directory)}
        if a.command == "status":
            row = self.db.execute("SELECT value FROM config WHERE key='executor'").fetchone()
            active = self.db.execute("SELECT * FROM jobs WHERE status IN ('running','interrupted')").fetchone()
            return {"executor": json.loads(row[0]) if row else None,
                    "state_dir": str(self.directory), "owner": self.public(active) if active else None,
                    "counts": dict(self.db.execute("SELECT status, count(*) FROM jobs GROUP BY status"))}
        binding = self.binding()
        if a.command == "submit":
            payload = read_json(a.request)
            for key in ("id", "objective", "target_app", "context", "success_condition", "authorization"):
                require_text(payload.get(key), key)
            requester = payload.get("requester")
            if not isinstance(requester, dict):
                raise ValueError("requester identity required")
            for key in ("threadId", "hostId"):
                require_text(requester.get(key), "requester." + key)
            if requester["hostId"] != binding["hostId"]:
                raise ValueError("requester must be on the executor's verified local host")
            text_list(payload.get("allowed_actions"), "allowed_actions")
            encoded = canonical(payload)
            old = self.db.execute("SELECT * FROM jobs WHERE id=?", (payload["id"],)).fetchone()
            if old:
                if old["payload"] != encoded:
                    raise ValueError("dedupe ID reused with a different payload")
                return {"duplicate": True, "job": self.public(old)}
            stamp = now()
            self.db.execute("INSERT INTO jobs (id,payload,status,created,updated) VALUES (?,?,'queued',?,?)",
                            (payload["id"], encoded, stamp, stamp))
            return {"duplicate": False, "job": self.public(self.job(payload["id"]))}
        if a.command == "claim":
            if {"threadId": a.executor, "hostId": a.host} != binding:
                raise ValueError("only the configured local executor may claim")
            active = self.db.execute("SELECT * FROM jobs WHERE status IN ('running','interrupted')").fetchone()
            if active:
                return {"claimed": False, "reason": "interrupted" if active["status"] == "interrupted" else "busy",
                        "owner_id": active["id"]}
            job = self.db.execute("SELECT * FROM jobs WHERE status='queued' ORDER BY seq LIMIT 1").fetchone()
            if not job:
                return {"claimed": False, "reason": "empty"}
            token = secrets.token_hex(24)
            self.db.execute("UPDATE jobs SET status='running',token=?,updated=? WHERE id=?", (token, now(), job["id"]))
            return {"claimed": True, "token": token, "job": self.public(self.job(job["id"]))}
        job = self.job(a.id)
        if a.command == "get":
            return self.public(job)
        if a.command == "wake":
            if job["status"] != "queued":
                return {"should_send": False, "id": a.id, "status": job["status"]}
            script = Path(__file__).resolve()
            prompt = (
                "Use $eruna as this computer's shared desktop executor. "
                f"Read {script.parents[1] / 'SKILL.md'} and its queue reference before acting. "
                f"Queue helper: {script}. State directory: {self.directory}. "
                f"Wake notification for queued job {a.id}; claim the oldest queued job, not necessarily this ID. "
                "Only a successful claim grants desktop ownership. Read its stored payload, verify scoped user "
                "authorization, and use the bundled computer-use skill. Do not resume unrelated prior work. "
                "Record actual actions, verified outcome, evidence and blocker via finish after input settles; "
                "then claim any remaining authorized jobs. If ownership is busy/interrupted, do no UI work. "
                "The requester pulls the stored result; do not send a callback. Preserve your model/thinking."
            )
            return {"should_send": True, "tool": "send_message_to_thread", "arguments": {**binding, "prompt": prompt}}
        if a.command == "finish":
            if job["status"] != "running" or not secrets.compare_digest(job["token"] or "", a.token):
                raise ValueError("not the running owner or wrong token; do not replay")
            result = read_json(a.result)
            text_list(result.get("actual_actions"), "actual_actions", nonempty=False)
            require_text(result.get("verified_outcome"), "verified_outcome")
            text_list(result.get("evidence"), "evidence", nonempty=a.status == "completed")
            if not isinstance(result.get("blocker"), str):
                raise ValueError("blocker must be text (empty on success)")
            if a.status != "completed":
                require_text(result["blocker"], "blocker")
            elif result["blocker"].strip():
                raise ValueError("use blocked/failed for an unresolved blocker")
            self.db.execute("UPDATE jobs SET status=?,result=?,token=NULL,updated=? WHERE id=?",
                            (a.status, canonical(result), now(), a.id))
        elif a.command == "interrupt":
            require_text(a.note, "note")
            if job["status"] not in ("running", "interrupted"):
                raise ValueError("only active ownership can be interrupted")
            self.db.execute("UPDATE jobs SET status='interrupted',note=?,updated=? WHERE id=?", (a.note, now(), a.id))
        elif a.command == "recover":
            require_text(a.note, "note")
            if job["status"] != "interrupted" or not a.confirm_stopped:
                raise ValueError("recovery requires interrupted ownership and confirmed stopped input")
            result = {"actual_actions": [], "verified_outcome": "Interrupted; partial UI outcome requires inspection.",
                      "evidence": [a.note], "blocker": "Recovered without replay: " + (job["note"] or "interrupted")}
            self.db.execute("UPDATE jobs SET status='failed',token=NULL,result=?,updated=? WHERE id=?",
                            (canonical(result), now(), a.id))
        elif a.command == "cancel":
            require_text(a.note, "note")
            if job["status"] != "queued":
                raise ValueError("only queued jobs can be cancelled; running jobs require interruption/recovery")
            self.db.execute("UPDATE jobs SET status='cancelled',note=?,updated=? WHERE id=?", (a.note, now(), a.id))
        return self.public(self.job(a.id))


def default_state_dir():
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    legacy = codex_home / "computer-task"
    current = codex_home / "eruna"
    if (legacy / "queue.sqlite3").exists():
        if (current / "queue.sqlite3").exists():
            raise ValueError("Both legacy and Eruna queues exist; reconcile explicitly without resetting either")
        return legacy
    return current


def parser():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--state-dir", default=str(default_state_dir()))
    sub = p.add_subparsers(dest="command", required=True)
    for name in ("init", "claim"):
        command = sub.add_parser(name)
        command.add_argument("--executor", required=True)
        command.add_argument("--host", required=True)
    sub.add_parser("status")
    command = sub.add_parser("submit")
    command.add_argument("--request", required=True)
    for name in ("get", "wake", "finish", "interrupt", "recover", "cancel"):
        command = sub.add_parser(name)
        command.add_argument("--id", required=True)
        if name == "finish":
            command.add_argument("--token", required=True)
            command.add_argument("--status", choices=("completed", "blocked", "failed"), required=True)
            command.add_argument("--result", required=True)
        if name in ("interrupt", "recover", "cancel"):
            command.add_argument("--note", required=True)
        if name == "recover":
            command.add_argument("--confirm-stopped", action="store_true")
    return p


def main():
    queue = None
    try:
        args = parser().parse_args()
        queue = Queue(args.state_dir)
        print(json.dumps(queue.run(args), ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, sqlite3.Error) as error:
        print(json.dumps({"error": str(error)}), file=sys.stderr)
        return 1
    finally:
        if queue:
            queue.close()


if __name__ == "__main__":
    sys.exit(main())
