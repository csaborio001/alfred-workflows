#!/usr/bin/env python3
"""
Alfred Script Filter for emoji search.
Usage: python3 emoji_search.py [query]

Outputs Alfred 5 JSON. On selection, the emoji symbol is passed to emoji_type.py
which types it directly into the frontmost app.
"""

import sys
import json
from emoji_data import EMOJI_SYMBOLS
from emoji_synonyms import expanded_words
from emoji_history import load_recent

RELATED_WORDS = expanded_words(EMOJI_SYMBOLS)


def fuzzy_match(word: str, query: str) -> bool:
    """Return True if query characters appear in order within word (case-insensitive)."""
    characters = iter(word.casefold())
    return all(any(character == candidate for candidate in characters)
               for character in query.casefold())


def score_match(name: str, query: str) -> int:
    """
    Score a match so better results sort first.
      3 = exact match
      2 = starts with query
      1 = contains query as substring
      0 = only fuzzy / related-word match
    """
    q = query.lower()
    n = name.lower()
    if n == q:
        return 3
    if n.startswith(q):
        return 2
    if q in n:
        return 1
    return 0


def search(query: str) -> list[dict]:
    query = query.strip().lstrip(':').lower()

    if not query:
        # Return full sorted list
        results = [(name, EMOJI_SYMBOLS[name], 1) for name in sorted(EMOJI_SYMBOLS)]
    else:
        seen: set[str] = set()
        scored: list[tuple[str, str, int]] = []

        for name, symbol in EMOJI_SYMBOLS.items():
            if fuzzy_match(name, query):
                s = score_match(name, query)
                scored.append((name, symbol, s))
                seen.add(name)

        # Also check related words
        for name, keywords in RELATED_WORDS.items():
            if name in seen:
                continue
            if name not in EMOJI_SYMBOLS:
                continue
            if any(fuzzy_match(kw, query) for kw in keywords):
                scored.append((name, EMOJI_SYMBOLS[name], 0))
                seen.add(name)

        # Sort: score desc, then name asc
        scored.sort(key=lambda x: (-x[2], x[0]))
        results = scored

    recent = {name: index for index, name in enumerate(load_recent())}
    results.sort(key=lambda item: (recent.get(item[0], len(recent)), -item[2], item[0]))

    items = []
    for name, symbol, *_ in results:
        related = RELATED_WORDS.get(name, [])
        subtitle_parts = [f":{name}:"]
        if name in recent:
            subtitle_parts.append("Recently used")
        if related:
            subtitle_parts.append("· " + ", ".join(related[:4]))

        items.append({
            "title": f"{symbol}  {name}",
            "subtitle": "  ".join(subtitle_parts) + "  — press ↵ to type, ⌘↵ to copy code",
            "arg": symbol,          # passed to emoji_type.py
            "variables": {
                "emoji_name": name,
                "emoji_symbol": symbol,
            },
            "mods": {
                "cmd": {
                    # ⌘+Enter copies the :code: instead
                    "arg": f":{name}:",
                    "subtitle": f"Copy :{name}: to clipboard",
                    "variables": {"copy_code": "true"},
                }
            },
            "text": {
                "copy": symbol,
                "largetype": f"{symbol}\n:{name}:",
            },
            "quicklookurl": "",
        })

    return items


def main() -> None:
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    items = search(query)
    output = {"items": items or [{
        "title": "No matching emojis",
        "subtitle": "Try a name or related word, such as happy, heart, or party.",
        "valid": False,
    }]}
    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()
