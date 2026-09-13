# Repair update — 2026-09-05

This update supersedes conflicting implementation details below.

- Backups: `~/Library/Application Support/WP Workflow Backups/20260905-142407/`.
- Repaired both the unsuffixed workspace and the Vicar Amelia-2 copy. Preserved each copy’s domains.txt and pages.txt. Other profiles were not changed.
- Both now connect site Script Filter → page Script Filter → Bash Run Script invoking `wp_open.rb`. The opener validates the URL and calls `/usr/bin/open -b org.mozilla.firefox -- URL` with separate arguments.
- All Ruby launch commands use workflow-relative paths and Bash (type 0), with input as argv. Both filters accept optional arguments.
- Removed disconnected legacy objects; restored wp-add and wp-del scripts and connections.
- Fixed page queries supplied as a single argv string. Missing site context now produces a non-actionable error instead of a relative URL.
- Runtime diagnostics: `~/Library/Logs/WP Site Shortcuts/workflow.jsonl`. Stages: sites, pages, pages_missing_domain, open_received, open_rejected, open_finished. Entries include the script directory and Alfred preferences environment variable. Shell tests also produce entries, distinguishable by absent alfred_preferences.
- Verified Ruby syntax, plist validity, connections, 27 sites, all page URLs for every site, query variants, missing-domain handling, and add/duplicate/delete using temporary data.
- Runtime confirmed the ACTIVE profile is the unsuffixed Alfred.alfredpreferences, contrary to the original handoff. Its missing page-to-opener connection was repaired. Alfred reload and search succeeded after an initial timeout. The sites log contains the unsuffixed alfred_preferences path. The direct opener test succeeded (exit 0). Full keyboard selection remains for the user to verify; the foreground app was Code when automation checked, so no keys were sent.
- User confirmed the complete site → page → Firefox flow works. See README.md for domain and page management instructions.

---

# Original handoff (historical)

# WordPress Alfred Workflow Handoff

## Intended flow

1. Type `wp` in Alfred.
2. The first Script Filter reads `domains.txt` and shows site shortcuts.
3. Select a site and press Enter.
4. The second Script Filter reads `pages.txt` and shows page shortcuts for that site.
5. Select a page and press Enter.
6. The page URL should open in Firefox.

Domain management keywords are intended to be:

- `wp-add shortcut https://example.com`
- `wp-del shortcut`

## Active Alfred profile

Alfred is configured to use this sync folder:

```text
~/Library/CloudStorage/OneDrive-Personal/Application Settings/Alfred
```

The active profile is:

```text
Alfred.alfredpreferences-Vicar Amelia-2
```

The active workflow is:

```text
Alfred.alfredpreferences-Vicar Amelia-2/workflows/user.workflow.7210C896-4D98-48B6-A5B1-81AC1A84FB87
```

This matters: the unsuffixed `Alfred.alfredpreferences` folder was edited first, but Alfred was actually loading the `Vicar Amelia-2` profile. The active profile originally had the old `word` workflow and did not contain the Ruby scripts.

## Active graph

```text
UID 765FD8C9-18D5-46F9-BA0D-1EF1468BF9B1
Script Filter keyword: wp
Script: wp_actions.rb
    |
    v
UID 8E1B4C72-3D90-46A5-B7F2-1C6E9A0D5B33
Script Filter: wp_pages.rb
    |
    v
UID BF8D8762-B8F9-4710-A856-95E11CC9E5B5
Open URL action: {query}, browser org.mozilla.firefox
```

The old object `E679835C-9F20-49A4-AF4B-BC3B6898B9B5` remains in the active plist but is disconnected. It is the original Bash two-shortcut URL builder and contains hardcoded paths to the unsuffixed profile. It should be removed to reduce ambiguity.

## Data files

`domains.txt` format:

```text
shortcut https://example.com
```

`pages.txt` format:

```text
shortcut /wp-admin/path
```

The parsers split each line into two whitespace-separated fields, preserving the remainder as the URL/path value. Blank lines and lines beginning with `#` are ignored.

## Script behavior

### `wp_actions.rb`

- Reads `domains.txt` relative to its own script directory.
- Joins Alfred arguments and lowercases/splits them into search terms.
- Filters sites by shortcut or domain URL.
- Emits Alfred JSON items with:
  - `uid`: site shortcut
  - `title`: site shortcut
  - `subtitle`: domain URL
  - `arg`: site shortcut
  - `variables.wp_domain`: domain URL
  - `type`: `default`
  - `valid`: `true`

The script returns 27 site items when run directly with no query.

### `wp_pages.rb`

- Reads `pages.txt` and `domains.txt` relative to its own script directory.
- Uses `ENV["wp_domain"]` if Alfred passes the workflow variable.
- Also searches Alfred arguments for a domain shortcut or full domain URL as a fallback.
- Removes the selected site token from the page search query.
- Constructs URLs by joining the domain and page path with exactly one slash.
- Emits page items with a full URL in `arg`, for example:

```text
https://saferbaby.org.au/wp-admin
```

The active script was tested with `sb admin` and `admin sb`; both produce the full URL when run directly.

## Confirmed facts

These checks have passed against the active profile:

- `plutil -lint info.plist`
- Ruby syntax checks for both scripts
- Active graph has no dangling connection targets
- Site script returns 27 sites
- Page script returns a full URL for `sb admin`
- Firefox can open the URL directly using:

```sh
open -a "Firefox" -- "https://saferbaby.org.au/wp-admin"
```

- The active page-to-opener connection is present.
- The active opener is Alfred's native Open URL action:

```text
browser: org.mozilla.firefox
url: {query}
version: 1
```

## Known problems / likely remaining failure

The user reports that site and page lists can appear, but selecting a page does not open anything. The unresolved boundary is therefore Alfred's runtime handoff from the page Script Filter item to the Open URL action.

The page script emits the URL correctly in shell tests, but shell tests do not prove that Alfred is passing the selected item's `arg` into `{query}`. The next agent should instrument or replace only this boundary.

Recommended diagnostic sequence:

1. In Alfred's debugger, inspect the page Script Filter output after selecting a page. Confirm the selected item has the full URL in `arg`.
2. Temporarily replace the Open URL action with a Script Action that appends `$1` to a log file, for example:

```sh
printf '<%s>\\n' "$1" >> /tmp/wp-alfred-action.log
```

3. Select a page and inspect `/tmp/wp-alfred-action.log`.
4. If the log is empty, the page filter connection or Alfred selection handoff is wrong.
5. If the log contains the URL, the Open URL action/browser configuration is the problem.
6. If the log contains a shortcut instead of a URL, the page Script Filter's `arg` is not the active profile/script being executed.

## Other issues to clean up

- Remove disconnected object `E679835C-9F20-49A4-AF4B-BC3B6898B9B5`.
- Keep only one active workflow profile; the OneDrive folder contains multiple profile copies (`Alfred.alfredpreferences`, `-Vicar Amelia`, `-Vicar Amelia-2`, and `-Micolash`).
- A separate workflow originally owned the `wp` keyword for WordPress Plugins. In the active profile it was renamed to `wpp`; verify that this change is not overwritten by OneDrive sync.
- The unsuffixed workspace copy and the active `Vicar Amelia-2` copy have diverged. Any future edits must target the active profile or deliberately synchronize both.
- `wp-add.rb` and `wp-delete.rb` were created in the original workflow directory; verify they also exist and are wired in the active profile before testing domain management.

## Important distinction

The scripts, data parsing, URL construction, and direct Firefox launch all work outside Alfred. The unresolved problem is not WordPress or the text files. It is the Alfred workflow runtime boundary, most likely the selected Script Filter item's `arg` not reaching the final action or Alfred loading a different profile copy than the one being edited.
