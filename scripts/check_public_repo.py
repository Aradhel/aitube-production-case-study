"""Fail when a public case-study repository contains obvious private artifacts."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

BLOCKED_SUFFIXES = {
    ".db", ".sqlite", ".sqlite3", ".pem", ".p12", ".pfx",
    ".ckpt", ".pth", ".pt", ".onnx", ".safetensors",
    ".wav", ".mp3", ".mp4", ".webm", ".mov",
}

BLOCKED_NAMES = {
    ".env", "credentials.json", "secrets.json", "id_rsa", "id_ed25519",
}

ALLOWED_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

TEXT_PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}\b"),
    "Stripe live secret": re.compile(r"\bsk_live_[A-Za-z0-9]{16,}\b"),
    "generic assigned secret": re.compile(
        r"(?i)\b(?:api[_-]?key|secret[_-]?key|access[_-]?token|password)\b\s*[:=]\s*['\"][^'\"]{8,}['\"]"
    ),
}


def iter_files() -> list[Path]:
    return [
        path for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts
    ]


def main() -> int:
    findings: list[str] = []

    for path in iter_files():
        relative = path.relative_to(ROOT)
        if path.name.lower() in BLOCKED_NAMES or path.suffix.lower() in BLOCKED_SUFFIXES:
            findings.append(f"blocked artifact: {relative}")
            continue

        if path.suffix.lower() in ALLOWED_IMAGE_SUFFIXES:
            continue

        if path.stat().st_size > 2_000_000:
            findings.append(f"unexpected large file: {relative}")
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append(f"unexpected binary file: {relative}")
            continue

        for label, pattern in TEXT_PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{label}: {relative}")

    if findings:
        print("Public repository check failed:")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print("Public repository check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
