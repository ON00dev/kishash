#!/usr/bin/env python3
"""
kishash.py
CLI tool to generate and validate 'hash.hex' files that contain an embedded secret key.

Usage:
  python kishash.py generate
  python kishash.py validate
  python kishash.py generate --file other.hex
  python kishash.py validate --file other.hex --key abc123...
"""

import secrets
import string
import argparse
from pathlib import Path
from typing import Optional, List

# Fixed configuration
POSITIONS: List[int] = [0, 4, 8, 16, 32, 64, 96, 112, 120, 127]
LINE_LENGTH = 128
NUM_LINES = 10
DEFAULT_FILENAME = "hash.hex"


def generate_secret_key() -> str:
    """Generate a 10-character hexadecimal secret key."""
    # token_hex(5) -> 10 hex characters
    return secrets.token_hex(5)


def random_hex_line() -> str:
    """Generate a random hex line of LINE_LENGTH characters (0-9a-f)."""
    # token_hex(64) -> 128 hex characters
    return secrets.token_hex(LINE_LENGTH // 2)


def write_file_with_key(secret_key: str, filename: str = DEFAULT_FILENAME) -> None:
    """Create the file with NUM_LINES lines, embedding secret_key characters at fixed positions."""
    if len(secret_key) != NUM_LINES:
        raise ValueError(f"secret_key must be exactly {NUM_LINES} hex characters")

    lines: List[str] = []
    for i in range(NUM_LINES):
        line = random_hex_line()
        pos = POSITIONS[i]
        # Replace the character at the fixed position with the corresponding key char
        line = line[:pos] + secret_key[i] + line[pos + 1:]
        lines.append(line)

    Path(filename).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n[OK] File '{filename}' written successfully.")
    print(f"[OK] Generated secret key: {secret_key}\n")


def extract_key_from_file(filename: str = DEFAULT_FILENAME) -> str:
    """Read the file and extract the secret key from the fixed positions."""
    p = Path(filename)
    if not p.exists():
        raise FileNotFoundError(f"File '{filename}' not found.")

    content = p.read_text(encoding="utf-8").splitlines()
    if len(content) != NUM_LINES:
        raise ValueError(f"File must contain {NUM_LINES} lines but contains {len(content)}")

    extracted_chars: List[str] = []
    for i, line in enumerate(content):
        if len(line) != LINE_LENGTH:
            raise ValueError(f"Line {i+1} has {len(line)} characters; expected {LINE_LENGTH}.")
        extracted_chars.append(line[POSITIONS[i]])

    return "".join(extracted_chars)


def cmd_generate(args: argparse.Namespace) -> None:
    key = generate_secret_key()
    write_file_with_key(key, args.file)


def cmd_validate(args: argparse.Namespace) -> None:
    try:
        extracted = extract_key_from_file(args.file)
    except Exception as e:
        print(f"[X] Error: {e}")
        return

    print(f"🔍 Extracted key: {extracted}")
    if args.key:
        if args.key == extracted:
            print("[OK] The provided key MATCHES the file.\n")
        else:
            print("[X] The provided key DOES NOT MATCH the file.\n")
    else:
        print("[!] No key provided for comparison. Extraction finished.\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="CLI to generate and validate a hash.hex file with an embedded secret key."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen = subparsers.add_parser("generate", help="Generate a new hash file")
    gen.add_argument("--file", "-f", default=DEFAULT_FILENAME, help="Output filename (default: hash.hex)")

    val = subparsers.add_parser("validate", help="Validate / extract key from a hash file")
    val.add_argument("--file", "-f", default=DEFAULT_FILENAME, help="Input filename (default: hash.hex)")
    val.add_argument("--key", "-k", help="Optional key to compare against the extracted key")

    args = parser.parse_args()

    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "validate":
        cmd_validate(args)


if __name__ == "__main__":
    main()
