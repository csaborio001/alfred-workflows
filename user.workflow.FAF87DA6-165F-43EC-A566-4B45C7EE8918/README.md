## Quick start

- Type `emo ` to list every emoji in the bundled collection.
- Continue typing, for example `emo happy`, to filter by name or related words.
- Press Return to paste the selected emoji into the frontmost app.
- Recently used emojis appear first, newest first, including among search matches.
  The last 100 distinct choices are saved in `recent_emojis.json` in this folder.
  Delete that file to reset the history. Browsing alone does not change history.
- Extra synonyms include `cheerful`, `exhausted`, `congrats`, `work`, `coding`,
  `grateful`, `holiday`, and `delicious`. Edit `emoji_synonyms.py` to add more.

The Script Filter accepts an optional argument. Both scripts use paths relative
to this workflow folder, so moving the Alfred preferences folder is supported.

# Alfred Emoji Workflow (Python)

Search emoji by name or related keyword, then **type** the symbol directly into
the frontmost app — no clipboard round-trip required.

---

## Files

| File | Purpose |
|---|---|
| `emoji_data.py` | All emoji symbols + related keywords (auto-generated from the original Ruby files) |
| `emoji_search.py` | Alfred **Script Filter** — fuzzy-searches emoji, returns JSON |
| `emoji_type.py` | Alfred **Run Script** action — types or copies the selected emoji |

---

## Alfred Setup

### 1. Create a new Workflow in Alfred

Preferences → Workflows → **+** → Blank Workflow  
Name it "Emoji" and set a keyword (e.g. `emoji` or `:`).

### 2. Add a Script Filter object

- **Language**: `/usr/bin/python3`
- **Script**:
  ```
  python3 /path/to/emoji_search.py "{query}"
  ```
- **Argument**: Optional (shows all emoji with no query)
- Check **"Run behaviour: Sequentially"** and set a short delay (~0.1 s) so it
  doesn't fire on every keypress.

### 3. Add a Run Script object

Connect Script Filter → Run Script.

- **Language**: `/usr/bin/python3`
- **Script**:
  ```
  python3 /path/to/emoji_type.py "{query}"
  ```

That's it. Alfred passes the selected item's `arg` (the emoji symbol) as
`{query}` to the Run Script.

---

## Usage

| Action | Shortcut | Result |
|---|---|---|
| Type emoji into current app | `↵` | 😄 typed into frontmost app |
| Copy `:emoji_code:` to clipboard | `⌘↵` | `:smile:` copied |

### Searching

- Type part of the emoji name: `lol` → matches `joy`, `laughing`, `rofl`, etc.
- Related words: `party` → balloon, tada, confetti_ball, beers, ...
- Fuzzy matching: `hrt` → heart, broken_heart, two_hearts, ...

---

## How the "type into app" trick works

`emoji_type.py` uses AppleScript to:
1. Set the clipboard to the emoji character
2. Send `⌘V` to `System Events`

This approach handles complex Unicode (multi-codepoint emoji, ZWJ sequences,
flag emoji) reliably across all macOS apps — even those that don't support direct
`keystroke` with Unicode.

> **Required permission**: System Preferences → Privacy & Security →
> Accessibility — Alfred must be allowed to control your computer.

---

## Requirements

- macOS (AppleScript + `pbcopy` are built in)
- Python 3.9+ (ships with macOS, or use Homebrew)
- Alfred 4 or 5 with Powerpack

No third-party Python packages needed.
