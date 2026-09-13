#!/usr/bin/env python3
"""
Alfred Run Script action for emoji workflow.

Behaviour:
  - ↵          types the emoji directly into the frontmost app
  - ⌘↵         adds the emoji to a buffer (shows count notification)
  - keyword 'emog' → types all buffered emoji, then clears the buffer
"""

import os
import sys
import subprocess
import tempfile
from emoji_history import record_use
from emoji_data import EMOJI_SYMBOLS

# Buffer file lives in /tmp so it's cleared on reboot automatically
BUFFER_FILE = os.path.join(tempfile.gettempdir(), "alfred_emoji_buffer.txt")


def type_into_frontmost(text: str) -> None:
    safe = text.replace('\\', '\\\\').replace('"', '\\"')
    script = f'''
        set the clipboard to "{safe}"
        tell application "System Events"
            keystroke "v" using command down
        end tell
    '''
    subprocess.run(["osascript", "-e", script], check=True)


def notify(title: str, msg: str) -> None:
    script = f'display notification "{msg}" with title "{title}"'
    subprocess.run(["osascript", "-e", script])


def add_to_buffer(emoji: str) -> None:
    with open(BUFFER_FILE, "a", encoding="utf-8") as f:
        f.write(emoji)
    current = read_buffer()
    count = len(current)
    notify("Emoji Buffer", f"Added {emoji}  →  buffer: {current}  ({count} emoji)")


def read_buffer() -> str:
    if not os.path.exists(BUFFER_FILE):
        return ""
    with open(BUFFER_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()


def clear_buffer() -> None:
    if os.path.exists(BUFFER_FILE):
        os.remove(BUFFER_FILE)


def flush_buffer() -> None:
    """Type all buffered emoji into the frontmost app, then clear."""
    text = read_buffer()
    if not text:
        notify("Emoji Buffer", "Buffer is empty — nothing to type!")
        return
    type_into_frontmost(text)
    clear_buffer()


def main() -> None:
    arg = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else ""

    # 'emog' keyword calls this script with --flush
    if arg == "--flush":
        flush_buffer()
        return

    if not arg:
        sys.exit(0)

    copy_code = os.environ.get("copy_code", "").lower() == "true"

    if copy_code:
        # ⌘↵: add to buffer
        add_to_buffer(arg)
    else:
        # ↵: type immediately
        type_into_frontmost(arg)

    name = os.environ.get("emoji_name", "")
    if EMOJI_SYMBOLS.get(name) != arg:
        name = next((name for name, symbol in EMOJI_SYMBOLS.items() if symbol == arg), "")
    record_use(name)


if __name__ == "__main__":
    main()