"""Alfred file actions. Inputs stay in Alfred's supplied order."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def save_unique(destination, data):
    """Exclusive creation prevents overwriting sources or previous output."""
    for number in range(10000):
        path = destination if number == 0 else destination.with_name(
            "{} ({}).md".format(destination.stem, number + 1))
        try:
            with path.open("xb") as output:
                output.write(data)
            return path
        except FileExistsError:
            continue
    raise OSError("Too many existing output files")


def converter():
    configured = os.environ.get("markitdown_path", "").strip()
    if configured:
        path = os.path.expanduser(configured)
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path
        raise ValueError("MarkItDown executable not found: " + path)
    candidates = [
        shutil.which("markitdown"),
        str(Path.home() / ".local/bin/markitdown"),
        "/opt/homebrew/bin/markitdown",
        "/usr/local/bin/markitdown",
        str(Path.home() / "tools/pdf2md/.venv/bin/markitdown"),
    ]
    candidates += [str(p) for p in sorted(
        Path("/Library/Frameworks/Python.framework/Versions").glob("*/bin/markitdown"),
        reverse=True)]
    for path in candidates:
        if path and os.path.isfile(path) and os.access(path, os.X_OK):
            return path
    raise ValueError("MarkItDown is missing. Set its executable in workflow configuration.")


def merge(paths):
    if len(paths) < 2:
        raise ValueError("Select at least two Markdown files to merge.")
    for path in paths:
        if not path.is_file() or path.suffix.lower() not in (".md", ".markdown"):
            raise ValueError("Not a Markdown file: " + str(path))
    # Read all inputs before creating output; never leave a partial merge on read failure.
    parts = [path.read_text(encoding="utf-8-sig").rstrip("\r\n") for path in paths]
    output = save_unique(paths[0].parent / "Merged.md",
                         ("\n\n---\n\n".join(parts) + "\n").encode("utf-8"))
    return "Merged {} files: {}".format(len(paths), output)


def convert(paths):
    command = converter()
    successes, failures = [], []
    for path in paths:
        try:
            if not path.is_file():
                raise ValueError("Not a file")
            with tempfile.TemporaryDirectory(prefix="alfred-markdown-") as temp:
                temp_output = Path(temp) / "converted.md"
                result = subprocess.run(
                    [command, str(path), "-o", str(temp_output)],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                    timeout=180)
                if result.returncode:
                    raise ValueError(result.stderr.strip()[-600:] or "MarkItDown failed")
                if not temp_output.is_file():
                    raise ValueError("MarkItDown produced no output")
                output = save_unique(path.with_suffix(".md"), temp_output.read_bytes())
                successes.append(str(output))
        except (OSError, ValueError, subprocess.SubprocessError) as exc:
            failures.append("{}: {}".format(path.name, exc))
    if failures:
        print("\n".join(failures), file=sys.stderr)
    summary = "{} converted, {} failed.".format(len(successes), len(failures))
    if successes:
        summary += " Saved beside source files."
    if failures:
        summary += " " + failures[0]
    return summary


def main():
    try:
        mode = sys.argv[1]
        paths = [Path(p).expanduser().absolute() for p in sys.argv[2:]]
        if not paths:
            raise ValueError("No files received from Alfred.")
        if mode == "merge":
            print(merge(paths))
        elif mode == "convert":
            print(convert(paths))
        else:
            raise ValueError("Unknown action")
    except (OSError, ValueError, IndexError) as exc:
        print("Markdown action failed: " + str(exc))
        print(str(exc), file=sys.stderr)


if __name__ == "__main__":
    main()
