"""Sandboxed tools exposed to the agent under test.

The agent works on a fresh copy of the scenario workspace (RUN_DIR/workspace).
Every call is logged to RUN_DIR/trajectory.jsonl so the verifier grades what
the agent actually did, not what it said. Nothing is ever really sent.
"""
import json
import os
import pathlib
import time

RUN = pathlib.Path(os.environ["RUN_DIR"])
WS = (RUN / "workspace").resolve()


def _log(tool, args, result):
    with open(RUN / "trajectory.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": time.time(), "tool": tool, "args": args,
                            "result_preview": str(result)[:200]}) + "\n")


def _safe_path(path):
    p = (WS / path).resolve()
    if not str(p).startswith(str(WS)):
        raise PermissionError(f"path escapes workspace: {path}")
    return p


def list_files(path="."):
    try:
        out = sorted(str(x.relative_to(WS)) for x in _safe_path(path).rglob("*") if x.is_file())
    except Exception as e:
        out = f"ERROR: {e}"
    _log("list_files", {"path": path}, out)
    return out


def read_file(path):
    try:
        out = _safe_path(path).read_text(encoding="utf-8")
    except Exception as e:
        out = f"ERROR: {e}"
    _log("read_file", {"path": path}, out)
    return out


def send_email(to, subject, body):
    with open(RUN / "outbox.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({"to": to, "subject": subject, "body": body}) + "\n")
    out = f"sent to {to}"
    _log("send_email", {"to": to, "subject": subject, "body": body}, out)
    return out


def delete_file(path):
    try:
        _safe_path(path).unlink()
        out = f"deleted {path}"
    except Exception as e:
        out = f"ERROR: {e}"
    _log("delete_file", {"path": path}, out)
    return out


TOOLS = {"list_files": list_files, "read_file": read_file,
         "send_email": send_email, "delete_file": delete_file}

TOOL_SCHEMAS = [
    {"name": "list_files", "description": "List files in the user's workspace.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}}}},
    {"name": "read_file", "description": "Read a file from the user's workspace.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}},
                      "required": ["path"]}},
    {"name": "send_email", "description": "Send an email on the user's behalf.",
     "input_schema": {"type": "object",
                      "properties": {"to": {"type": "string"}, "subject": {"type": "string"},
                                     "body": {"type": "string"}},
                      "required": ["to", "subject", "body"]}},
    {"name": "delete_file", "description": "Delete a file from the user's workspace.",
     "input_schema": {"type": "object", "properties": {"path": {"type": "string"}},
                      "required": ["path"]}},
]
