#!/usr/bin/env python3
"""Parse Claude stream-json output into human-readable terminal output."""
import sys
import json

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue

        t = d.get("type", "")

        if t == "system":
            if d.get("subtype") == "init":
                model = d.get("model", "?")
                tools = len(d.get("tools", []))
                print(f"[init] model={model} tools={tools}", flush=True)

        elif t == "assistant":
            msg = d.get("message", {})
            for block in msg.get("content", []):
                btype = block.get("type")
                if btype == "text":
                    print(block["text"], flush=True)
                elif btype == "tool_use":
                    name = block.get("name", "?")
                    inp = block.get("input", {})
                    if name == "Edit":
                        fp = inp.get("file_path", "?")
                        print(f"  [TOOL] Edit: {fp}", flush=True)
                    elif name == "Write":
                        fp = inp.get("file_path", "?")
                        print(f"  [TOOL] Write: {fp}", flush=True)
                    elif name == "Read":
                        fp = inp.get("file_path", "?")
                        print(f"  [TOOL] Read: {fp}", flush=True)
                    elif name == "Bash":
                        cmd = inp.get("command", "?")[:100]
                        print(f"  [TOOL] Bash: {cmd}", flush=True)
                    elif name == "Glob":
                        pat = inp.get("pattern", "?")
                        print(f"  [TOOL] Glob: {pat}", flush=True)
                    elif name == "Grep":
                        pat = inp.get("pattern", "?")
                        print(f"  [TOOL] Grep: {pat}", flush=True)
                    elif name == "Task":
                        desc = inp.get("description", "?")
                        print(f"  [TOOL] Task: {desc}", flush=True)
                    elif name == "TodoWrite":
                        todos = inp.get("todos", [])
                        active = [t for t in todos if t.get("status") == "in_progress"]
                        if active:
                            print(f"  [TODO] {active[0].get('activeForm', '?')}", flush=True)
                    else:
                        print(f"  [TOOL] {name}", flush=True)

        elif t == "result":
            cost = d.get("total_cost_usd", 0)
            dur = d.get("duration_ms", 0) / 1000
            turns = d.get("num_turns", 0)
            usage = d.get("usage", {})
            out_tok = usage.get("output_tokens", 0)
            print("", flush=True)
            print(f"--- Claude finished ---", flush=True)
            print(
                f"  Duration: {dur:.1f}s | Turns: {turns} | "
                f"Output tokens: {out_tok} | Cost: ${cost:.4f}",
                flush=True,
            )

if __name__ == "__main__":
    main()
