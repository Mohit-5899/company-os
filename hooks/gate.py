#!/usr/bin/env python3
"""company-os approval gate.

pre    (PreToolUse): deny outbound tools (send, publish, post, push to main, orders)
       unless the owner opened the gate in the last GATE_MINUTES.
prompt (UserPromptSubmit): a prompt starting with "approve" or "/company-os:approve"
       opens the gate.

Does nothing until the plugin is configured with a company folder.
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

GATE_MINUTES = 15  # ponytail: one global window, per-item tokens if a window proves too loose

# Last segment of the tool name (after the final "__"). Covers Gmail, Zernio, Buffer-style
# and broker tools; add more in config.json "extra_outbound".
OUTBOUND = {
    "send_message", "send_email", "send_draft", "reply", "forward",
    "posts_create", "posts_publish_now", "posts_cross_post", "posts_retry",
    "posts_retry_all_failed", "posts_bulk_upload_posts", "posts_edit_post",
    "posts_update", "posts_unpublish_post", "posts_delete",
    "comments_reply_to_inbox_post", "mentions_reply_to_mention",
    "create_post", "publish_post", "create_tweet", "post_tweet",
    "make_outbound_call", "share_file",
    "place_order", "modify_order", "place_gtt_order", "modify_gtt_order",
}
APPROVE_PROMPT = re.compile(r"^\s*/?(company-os:)?approve\b", re.IGNORECASE)
GIT_PUSH = re.compile(r"\bgit\s+push\b")
MAIN_BRANCH = re.compile(r"\b(main|master)\b")
PR_MERGE = re.compile(r"\bgh\s+pr\s+merge\b")


def company_dir():
    d = os.environ.get("CLAUDE_PLUGIN_OPTION_COMPANY_DIR", "").strip()
    return Path(d).expanduser() if d else None


def gate_file():
    data = os.environ.get("CLAUDE_PLUGIN_DATA") or str(Path.home() / ".claude/plugins/data/company-os")
    return Path(data) / "gate-open"


def load_config(cdir):
    try:
        return json.loads((cdir / "config.json").read_text())
    except (OSError, ValueError):
        return {}


def gate_is_open():
    try:
        return time.time() - gate_file().stat().st_mtime < GATE_MINUTES * 60
    except OSError:
        return False


def current_branch(cwd):
    try:
        out = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd or None,
                             capture_output=True, text=True, timeout=5)
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def is_outbound(tool, inp, cwd, config):
    if tool == "Bash":
        cmd = inp.get("command", "")
        if PR_MERGE.search(cmd):
            return True
        if GIT_PUSH.search(cmd):
            return bool(MAIN_BRANCH.search(cmd)) or current_branch(cwd) in ("main", "master")
        return False
    name = tool.rsplit("__", 1)[-1]
    if name not in OUTBOUND and name not in set(config.get("extra_outbound", [])):
        return False
    if name == "posts_create" and inp.get("is_draft") is True:
        return False
    if name == "send_message" and not inp.get("draftId"):
        allowed = {e.lower() for e in config.get("allow_recipients", [])}
        rcpts = [r.lower() for k in ("to", "cc", "bcc") for r in inp.get(k) or []]
        if rcpts and allowed and set(rcpts) <= allowed:
            return False  # email to the owner's own inbox (standup, report)
    return True


def touches_gate(tool, inp):
    if tool == "Bash":
        return "gate-open" in inp.get("command", "")
    path = inp.get("file_path") or inp.get("notebook_path") or ""
    return path.endswith("gate-open")


def deny(reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason,
    }}))


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pre"
    cdir = company_dir()
    if not cdir:
        return
    event = json.load(sys.stdin)

    if mode == "prompt":
        if APPROVE_PROMPT.match(event.get("prompt", "")):
            gate_file().parent.mkdir(parents=True, exist_ok=True)
            gate_file().touch()
        return

    tool, inp = event.get("tool_name", ""), event.get("tool_input") or {}
    if touches_gate(tool, inp):
        deny("company-os: only the owner opens the approval gate, by typing 'approve <IDs>'.")
    elif is_outbound(tool, inp, event.get("cwd"), load_config(cdir)) and not gate_is_open():
        deny(f"company-os approval gate: '{tool}' sends, publishes or pushes. Don't retry. Draft it, add a "
             f"Pending row to {cdir / 'approvals.md'}, and tell the owner. It goes out after they type "
             f"'approve <ID>'.")


if __name__ == "__main__":
    main()
