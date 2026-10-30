# Queue commands and handoff

Run with the verified Python interpreter and the installed `scripts/computer_queue.py` path. Examples use `python <script>` as shorthand. Commands emit JSON; errors exit 1. Python's standard-library SQLite serializes mutations across processes. FIFO order is the committed sequence number, not caller timestamps. There is no daemon or MCP client in the helper.

## Bind and submit

`init --executor <verified-thread-id> --host <verified-host>` creates or reuses a binding. It refuses rebinding; do not reset a queue to fix discovery. `status` reports the binding, active ownership and job counts. `get --id <id>` reads the full request/result; it never exposes ownership tokens.

Requests are UTF-8 JSON files stored outside Git:

```json
{
  "id": "unique-authorized-attempt-id",
  "requester": {"threadId": "verified-calling-thread", "hostId": "verified-local-host"},
  "objective": "Read the Calculator display",
  "target_app": "Windows Calculator",
  "context": "A read-only check; do not change the calculation.",
  "allowed_actions": ["Inspect the Calculator window and its current display"],
  "success_condition": "Return the observed display text with UI evidence, or a concrete blocker.",
  "authorization": "The user explicitly requested this read-only delegated check in this chat."
}
```

`submit --request <file>` is atomic and idempotent for identical IDs/payloads. `wake --id <id>` emits `should_send` and supported `send_message_to_thread` arguments with only `threadId`, `hostId`, `prompt`. It never sends, changes model/thinking, or promises delivery. Terminal/running jobs do not need another wake. Each new queued submission should send a wake, even if the executor appears busy, so arrivals near its final empty check are not lost. Concurrent wakes may queue multiple chat turns; they do not grant ownership.

Use `get` as the durable pull-result channel. `wait_threads` observes the chat; it does not observe/complete arbitrary local job IDs. No callback is sent automatically. If tools are unavailable, report the queued job and pasteable wake prompt. A stopped app/host needs a later explicit wake; no background availability is claimed.

## Execute and release

`claim --executor <bound-thread> --host <bound-host>` returns one of `claimed`, `busy`, `interrupted`, `empty`. A successful response includes the payload, ID and a random `token`. Identity arguments are a cooperative check, not authenticated caller identity. Keep the token out of handoffs and screenshots.

Result files:

```json
{
  "actual_actions": ["Inspected Calculator's current UI without changing its state"],
  "verified_outcome": "Observed display: 0",
  "evidence": ["Fresh UI accessibility observation or a local screenshot reference"],
  "blocker": ""
}
```

`finish --id <id> --token <token> --status completed --result <file>` stores the result and releases the desktop in the same transaction. Also supports `blocked` and `failed`. A blocked/failed result requires a nonempty blocker; completion requires evidence. Report uncertainty honestly. A blocked job releases only after all UI input has stopped; a resumed authorized attempt uses a new ID linked in context and starts from fresh UI state.

`cancel --id <queued-id> --note <reason>` cancels only a queued job. It cannot release a running job. Read/cancel only within the user's authorized coordination scope.

## Interruptions and recovery

1. `interrupt --id <active-id> --note <reason>` marks the owner interrupted and retains the exclusive slot. Use after a crash/uncertain UI activity, missing token or cancelled turn. Inspection by an authorized coordinator may mark it; it cannot release or execute anything. Never infer a crash just from `notLoaded` or an idle snapshot.
2. Inspect that exact executor's latest dispatched turn and any outstanding UI calls. Establish that the old turn and input have stopped. If you cannot prove this, leave the slot held and report it. Ask the user only when their intervention is actually needed to stop/confirm it.
3. Only after verified quiescence, `recover --id <id> --confirm-stopped --note <concrete-evidence>` closes it as `failed`, records recovery evidence and releases the slot. No time-based expiry, automatic requeue or UI replay occurs. Recovery needs explicit evidence, not merely elapsed time. It is an operational assertion that the CLI cannot independently verify.
4. Pull/report any partial outcome. A retry requires a newly authorized attempt based on observed current UI state, with a new ID referencing the interrupted one. Wake the queue to process remaining jobs.

## Local files and validation

Default state: `<CODEX_HOME>/computer-task/queue.sqlite3`, otherwise `~/.codex/computer-task/queue.sqlite3`. Runtime files must stay outside any Git checkout or skill directory. `--state-dir <absolute-private-directory>` is for isolated tests or an explicitly selected single shared location; all live requesters must use the same default location. Never create per-project live queues for the same desktop. Binding IDs and relative `local` host labels apply only to this machine; do not migrate them.

`python -m unittest discover -s <skill>/scripts -p test_computer_queue.py` runs isolated temporary-directory tests, including concurrent submissions/claims, dedupe, FIFO, ownership fencing, persistence and interruption recovery. No real UI work is performed by those tests.
