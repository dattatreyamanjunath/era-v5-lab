"""Run the era-v5-lab pr-guard rules locally on staged files (git diff --cached).

Mirrors .github/workflows/pr-guard.yml: team/topic path, file size <= 5 MB,
no data/model/archive extensions, no secrets or email addresses in added lines.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys

TEAM = "04-ke2"
MAX_BYTES = 5 * 1024 * 1024
BAD_EXT = re.compile(r"\.(parquet|arrow|zst|gz|zip|tar|bin|pt|safetensors)$", re.I)
SECRET = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "an AWS key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "a private key"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"), "a GitHub token"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}"), "an API key"),
    (re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"), "a Slack token"),
    (re.compile(r"[A-Za-z0-9._%+-]+@(?!users\.noreply\.github\.com|example\.(com|org))[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
     "an email address"),
]


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def main() -> int:
    root = git("rev-parse", "--show-toplevel").strip()
    os.chdir(root)
    files = [l for l in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if l]
    problems = []
    for f in files:
        p = f.split("/")
        if p[0] != "teams" or p[1] != TEAM or len(p) < 4:
            problems.append(f"{f}: must be under teams/{TEAM}/<topic>/")
        if BAD_EXT.search(f):
            problems.append(f"{f}: data/model/archive extension")
        if os.path.getsize(f) > MAX_BYTES:
            problems.append(f"{f}: larger than 5 MB ({os.path.getsize(f)} bytes)")
        added = "\n".join(l for l in git("diff", "--cached", "-U0", "--", f).splitlines()
                          if l.startswith("+") and not l.startswith("+++"))
        for rx, what in SECRET:
            m = rx.search(added)
            if m:
                problems.append(f"{f}: seems to contain {what}: {m.group(0)[:40]!r}")
    print(f"pr-precheck: {len(files)} staged files")
    for x in problems:
        print("  -", x)
    print("pr-precheck:", "PASS" if not problems else f"FAIL ({len(problems)})")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
