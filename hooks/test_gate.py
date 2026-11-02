"""Run: python3 hooks/test_gate.py"""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

GATE = Path(__file__).with_name("gate.py")


def run(mode, event, env):
    out = subprocess.run([sys.executable, str(GATE), mode], input=json.dumps(event),
                         capture_output=True, text=True, env=env, check=True)
    return "deny" in out.stdout


with tempfile.TemporaryDirectory() as tmp:
    cdir, data = Path(tmp, "company-os"), Path(tmp, "data")
    cdir.mkdir()
    (cdir / "config.json").write_text(json.dumps({"allow_recipients": ["me@co.com"]}))
    env = {**os.environ, "CLAUDE_PLUGIN_OPTION_COMPANY_DIR": str(cdir), "CLAUDE_PLUGIN_DATA": str(data)}
    gmail = "mcp__abc-123__send_message"

    def pre(tool, inp):
        return run("pre", {"tool_name": tool, "tool_input": inp, "cwd": tmp}, env)

    assert pre(gmail, {"to": ["client@x.com"], "subject": "hi"}), "send to client must be denied"
    assert not pre(gmail, {"to": ["ME@co.com"]}), "send to owner is allowed"
    assert pre(gmail, {"to": ["me@co.com"], "cc": ["client@x.com"]}), "cc to client must be denied"
    assert pre(gmail, {"draftId": "d1"}), "sending a draft must be denied"
    assert not pre("mcp__abc-123__create_draft", {"to": ["client@x.com"]}), "drafts are fine"
    assert pre("mcp__zernio__posts_create", {"content": "x", "platform": "x"}), "post must be denied"
    assert not pre("mcp__zernio__posts_create", {"content": "x", "platform": "x", "is_draft": True})
    assert not pre("mcp__zernio__posts_list", {}), "reads are fine"
    assert pre("Bash", {"command": "git push origin main"}), "push to main must be denied"
    assert not pre("Bash", {"command": "git push origin feature-x"}), "branch push is fine"
    assert pre("Bash", {"command": "gh pr merge 12"}), "merge must be denied"
    assert pre("Write", {"file_path": str(data / "gate-open")}), "agents can't open the gate"
    assert pre("Bash", {"command": f"touch {data}/gate-open"}), "agents can't open the gate"

    assert not run("prompt", {"prompt": "please approve everything"}, env)
    assert pre(gmail, {"to": ["client@x.com"]}), "approve mid-sentence must not open the gate"
    run("prompt", {"prompt": "approve A3 A5"}, env)
    assert not pre(gmail, {"to": ["client@x.com"]}), "open gate lets the send through"

    unconfigured = {**env, "CLAUDE_PLUGIN_DATA": str(Path(tmp, "other"))}
    unconfigured.pop("CLAUDE_PLUGIN_OPTION_COMPANY_DIR")
    assert not run("pre", {"tool_name": gmail, "tool_input": {"to": ["c@x.com"]}}, unconfigured), \
        "unconfigured plugin does nothing"

print("gate: all checks pass")
