# Notes and Markdown actions

Use `md query` in Alfred to search notes. Configure **Notes folder** to select the vault.

## Convert to Markdown (MarkItDown)

Select one or more files in Alfred, open their file actions, and choose **Convert to Markdown (MarkItDown)**. Each successful conversion creates a `.md` beside its source. If that name exists, a suffix such as ` (2)` is added. The original files are preserved.

MarkItDown must be installed with dependencies for the formats you want to convert. The workflow detects common Homebrew, pipx, Python framework, and the existing `~/tools/pdf2md/.venv` installations. Set **MarkItDown executable** in workflow configuration to override detection.

For a separate installation, using your installed Python:

```sh
/opt/homebrew/bin/python3 -m venv "$HOME/.local/share/alfred-markitdown"
"$HOME/.local/share/alfred-markitdown/bin/python" -m pip install 'markitdown[all]'
```

Then set **MarkItDown executable** to `~/.local/share/alfred-markitdown/bin/markitdown`. See [MarkItDown’s official instructions](https://github.com/microsoft/markitdown#installation) for supported formats and dependencies.

Conversions have a three-minute timeout per file. The notification reports successes/failures; detailed converter errors appear in Alfred’s debugger.

## Merge Markdown files

Select two or more `.md` or `.markdown` files in Alfred and choose **Merge Markdown files**.

- Inputs are joined in the order Alfred passes them, without sorting.
- The output is `Merged.md` beside the first input, or a numbered alternative if it exists.
- Sections are separated by a blank line, a Markdown horizontal rule (`---`), and another blank line.
- Files must be UTF-8 (a UTF-8 BOM is accepted). A read/validation failure prevents creation of the merged file.
- Original files remain intact. Front matter, headings, and relative links remain as written; links from files in different directories are not rebased.

Both actions accept multiple file arguments. The merge action is visible for all file selections so differently registered Markdown file types work; it validates the extensions before merging.

## Markdown from OCR

Select one or more PDF files in Alfred and choose **Markdown from OCR**. This is the former **OCR → Markdown (Spanish)** workflow, now included in Notes.

The original script invocation is preserved:

```sh
/usr/local/bin/python3 "$HOME/bin/ocr_md_single.py" "$@"
```

The helper script and its Python/OCR dependencies must be installed on each Mac. The original notification reports Markdown files in a `_markdown` folder beside the source; actual processing is controlled by that external helper. Migrating this action does not alter the helper or its Spanish OCR configuration.
