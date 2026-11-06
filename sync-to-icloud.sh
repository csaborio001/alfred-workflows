#!/bin/bash
# Publish local workflows to iCloud. Never copies data back to the local master.
set -euo pipefail
SOURCE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
DESTINATION='/Users/csaborio/Library/Mobile Documents/com~apple~CloudDocs/Application Settings/Alfred/Alfred.alfredpreferences/workflows'
options=(-rltpc --itemize-changes --stats)
dry_run=false
for argument in "$@"; do
    case "$argument" in
        --dry-run) options+=(--dry-run); dry_run=true ;;
        --mirror) options+=(--delete-after) ;;
        -h|--help)
            cat <<'HELP'
Usage: ./sync-to-icloud.sh [--dry-run] [--mirror]

Copies user.workflow.* folders from beside this script to the fixed iCloud
Alfred workflows folder. Local files win, even when iCloud files are newer.
--dry-run  Show planned changes without writing anything.
--mirror   Also delete destination workflow files/folders absent locally.

Git metadata, .DS_Store and Python bytecode caches are excluded and protected
from deletion. Other files outside workflow folders are left alone.
Uses checksums so same-size/same-date changes are detected. Symlinks are copied
as links, not followed. No Git commands, scheduling, or reverse sync occurs.
HELP
            exit 0 ;;
        *) echo "Unknown option: $argument (use --help)" >&2; exit 2 ;;
    esac
done
fail() { echo "Sync refused: $*" >&2; exit 1; }
[[ -d "$DESTINATION" && ! -L "$DESTINATION" ]] || fail 'Destination must be an existing real directory.'
resolved_destination="$(cd -- "$DESTINATION" && pwd -P)"
[[ "$SOURCE" != "$resolved_destination" ]] || fail 'Source and destination are the same.'
case "$SOURCE/" in "$resolved_destination/"*) fail 'Source is inside destination.' ;; esac
case "$resolved_destination/" in "$SOURCE/"*) fail 'Destination is inside source.' ;; esac
shopt -s nullglob
workflows=("$SOURCE"/user.workflow.*)
[[ ${#workflows[@]} -gt 0 ]] || fail 'No local workflows found.'
for workflow in "${workflows[@]}"; do
    [[ -d "$workflow" && ! -L "$workflow" && -f "$workflow/info.plist" ]] || fail "Invalid workflow: $workflow"
    /usr/bin/plutil -lint "$workflow/info.plist" >/dev/null || fail "Invalid plist: $workflow/info.plist"
done
# Refuse destination workflow symlinks rather than risk following aliases.
for workflow in "$DESTINATION"/user.workflow.*; do
    [[ ! -L "$workflow" ]] || fail "Destination workflow is a symlink: $workflow"
done
printf 'Source:      %s\nDestination: %s\n' "$SOURCE" "$DESTINATION"
if "$dry_run"; then echo 'DRY RUN: no files will be changed.'; fi
/usr/bin/rsync "${options[@]}" \
    --exclude='.git' --exclude='.DS_Store' \
    --exclude='__pycache__' --exclude='*.pyc' --exclude='*.pyo' \
    --include='/user.workflow.*/' --exclude='/*' \
    "$SOURCE/" "$DESTINATION/"
