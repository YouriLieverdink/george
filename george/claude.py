"""Claude Code CLI wrapper — conversation management via `claude -p`."""

from __future__ import annotations

import json
import subprocess
import sys


SONNET = "sonnet"
OPUS = "opus"

GEORGE_PREFIX = "\033[1mgeorge >\033[0m "


class Conversation:
    """Manages a multi-turn conversation with Claude via `claude -p`.

    All messages stream to the terminal via --output-format stream-json,
    capturing session_id from the first event for conversation continuity.
    """

    def __init__(self, model: str = SONNET):
        self.model = model
        self.session_id: str | None = None

    def send(self, user_content: str, system: str) -> str:
        """Send a message, stream the response, return full text."""
        cmd = ["claude", "-p", "--model", self.model,
               "--output-format", "stream-json",
               "--verbose", "--include-partial-messages",
               "--allowedTools", ""]

        if self.session_id:
            cmd.extend(["--resume", self.session_id])
        else:
            cmd.extend(["--system-prompt", system])

        return self._stream(cmd, user_content)

    def send_structured(self, user_content: str, system: str, tools: list[dict]) -> dict:
        """Send a message and get structured JSON response.

        Uses --json-schema for validation. Non-streaming since we need
        the complete JSON object.
        """
        tool = tools[0]
        schema = tool["input_schema"]
        tool_name = tool["name"]

        prompt = (
            f"{user_content}\n\n"
            f"---\n\n"
            f"Respond with ONLY a JSON object matching the `{tool_name}` schema. "
            f"No markdown fences, no explanation — just the raw JSON object."
        )

        cmd = ["claude", "-p", "--model", self.model,
               "--output-format", "json",
               "--json-schema", json.dumps(schema),
               "--allowedTools", ""]

        if self.session_id:
            cmd.extend(["--resume", self.session_id])
        else:
            cmd.extend(["--system-prompt", system])

        proc = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, timeout=180,
        )

        if proc.returncode != 0:
            print(f"claude error: {proc.stderr.strip()}", file=sys.stderr)
            return {}

        return self._parse_json_response(proc.stdout)

    def send_summary(self, system: str) -> str:
        """Generate a conversation summary (non-streaming)."""
        if self.session_id is None:
            return ""

        prompt = (
            "Summarize this conversation for the coaching log. Use the standard format:\n\n"
            "### Summary\n[2-3 sentence overview]\n\n"
            "### Key Points\n[bullet points of decisions, observations, data]\n\n"
            "### Action Items\n[bullet points of follow-ups]\n\n"
            "Be concise. Include specific numbers and dates. Write in the language the athlete used."
        )

        cmd = ["claude", "-p", "--resume", self.session_id,
               "--output-format", "text", "--allowedTools", ""]

        proc = subprocess.run(
            cmd, input=prompt, capture_output=True, text=True, timeout=60,
        )

        return proc.stdout.strip() if proc.returncode == 0 else ""

    def _stream(self, cmd: list[str], user_content: str) -> str:
        """Stream response via stream-json, print with george > prefix."""
        proc = subprocess.Popen(
            cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True,
        )

        proc.stdin.write(user_content)
        proc.stdin.close()

        collected: list[str] = []
        prefix_printed = False

        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue

            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Capture session_id from first event
            if self.session_id is None:
                sid = event.get("session_id")
                if sid:
                    self.session_id = sid

            # Stream text deltas
            inner = event.get("event", {})
            if (inner.get("type") == "content_block_delta"
                    and inner.get("delta", {}).get("type") == "text_delta"):
                text = inner["delta"]["text"]
                if not prefix_printed:
                    print(GEORGE_PREFIX, end="", flush=True)
                    prefix_printed = True
                print(text, end="", flush=True)
                collected.append(text)

        proc.wait()

        if prefix_printed:
            print()  # newline after streaming

        err = proc.stderr.read().strip()
        if proc.returncode != 0 and err:
            print(f"claude error: {err}", file=sys.stderr)

        return "".join(collected).strip()

    def _parse_json_response(self, stdout: str) -> dict:
        """Parse JSON from claude --output-format json response."""
        try:
            data = json.loads(stdout)
            if isinstance(data, dict):
                # Capture session_id
                if data.get("session_id") and self.session_id is None:
                    self.session_id = data["session_id"]

                result_text = data.get("result", stdout)
                if isinstance(result_text, str):
                    # Result is a JSON string — parse it
                    return json.loads(result_text)
                if isinstance(result_text, dict):
                    return result_text
            return data
        except (json.JSONDecodeError, TypeError):
            try:
                return json.loads(stdout)
            except json.JSONDecodeError:
                print(f"failed to parse structured output", file=sys.stderr)
                return {}
