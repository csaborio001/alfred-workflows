"""Persist the 100 most recently used emoji names beside the workflow scripts."""
import json
import os
import tempfile
from pathlib import Path

HISTORY_FILE = Path(__file__).with_name('recent_emojis.json')


def load_recent():
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding='utf-8'))
        if isinstance(data, list):
            return list(dict.fromkeys(name for name in data if isinstance(name, str)))[:100]
    except (OSError, ValueError):
        pass
    return []


def record_use(name):
    if not name:
        return
    recent = [name] + [item for item in load_recent() if item != name]
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=HISTORY_FILE.parent,
                                         prefix='.emoji-history-', delete=False) as stream:
            temporary = stream.name
            json.dump(recent[:100], stream, ensure_ascii=False)
        os.replace(temporary, HISTORY_FILE)
    except OSError:
        # A history write failure must not prevent inserting an emoji.
        pass
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)
