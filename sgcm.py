#!/usr/bin/env python3
import sys
import subprocess


def main():
    if len(sys.argv) < 2:
        print("Usage: sgcm <file_index> [file_index...]", file=sys.stderr)
        sys.exit(1)

    try:
        result = subprocess.run(
            ["git", "diff", "--name-only"], capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print("Error running git diff:", e, file=sys.stderr)
        sys.exit(1)

    files = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not files:
        print("No modified files found.", file=sys.stderr)
        sys.exit(1)

    selected = []
    for arg in sys.argv[1:]:
        if not arg.isdigit():
            print(f"Index '{arg}' is not a valid number.", file=sys.stderr)
            sys.exit(1)
        idx = int(arg) - 1
        if idx < 0 or idx >= len(files):
            print(f"Index '{arg}' is out of range (1-{len(files)}).", file=sys.stderr)
            sys.exit(1)
        if not files[idx]:
            print(f"File for index '{arg}' is empty.", file=sys.stderr)
            sys.exit(1)
        selected.append(files[idx])

    try:
        diff_proc = subprocess.run(
            ["git", "diff", "--"] + selected, capture_output=True, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print("Error running git diff on selected files:", e, file=sys.stderr)
        sys.exit(1)
    diff_output = diff_proc.stdout

    try:
        sgpt_proc = subprocess.run(
            ["sgpt", "Create a conventional commit style message for the changes"],
            input=diff_output,
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print("Error running sgpt:", e, file=sys.stderr)
        sys.exit(1)
    commit_msg = sgpt_proc.stdout

    try:
        subprocess.run(["git", "add"] + selected, check=True)
    except subprocess.CalledProcessError as e:
        print("Error staging files with git add:", e, file=sys.stderr)
        sys.exit(1)

    try:
        subprocess.run(
            ["git", "commit", "-F", "-"], input=commit_msg, text=True, check=True
        )
    except subprocess.CalledProcessError as e:
        print("Error committing changes:", e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
