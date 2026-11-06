# Publish workflows to iCloud

The local repository is authoritative. Run from any directory:

```sh
/Users/csaborio/code/alfred-workflows/sync-to-icloud.sh --dry-run
/Users/csaborio/code/alfred-workflows/sync-to-icloud.sh
```

Default behavior adds and updates workflow files. To also remove workflow files
and folders that have been deleted locally:

```sh
/Users/csaborio/code/alfred-workflows/sync-to-icloud.sh --mirror --dry-run
/Users/csaborio/code/alfred-workflows/sync-to-icloud.sh --mirror
```

Destination:
`/Users/csaborio/Library/Mobile Documents/com~apple~CloudDocs/Application Settings/Alfred/Alfred.alfredpreferences/workflows`

Only `user.workflow.*` directories are published. Git metadata, Finder metadata,
and Python bytecode are excluded; existing excluded files remain untouched.
Local workflow preferences and bundled data are copied too. Newer iCloud edits
are overwritten by the local master. No changes are copied back. This is a
publication script, not a versioned backup or a GitHub push.

The script validates local workflow plists and rejects an empty source or an
unsafe destination. Checksums catch files whose timestamps match despite changed
contents. Failed rsync operations return a nonzero exit status. Avoid running
concurrent copies. No daily schedule is installed.

At setup, Alfred's syncfolder still pointed to this iCloud preferences folder:
Alfred runs the published copy, so changes made in Alfred Preferences must be
manually brought into the local master before the next publication if desired.
