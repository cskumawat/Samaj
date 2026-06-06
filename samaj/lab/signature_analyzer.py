"""File hashing and signature helpers."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileSignature:
    md5: str
    sha1: str
    sha256: str
    size_bytes: int
    file_type: str


def analyze_signature(path: Path) -> FileSignature:
    data = Path(path).read_bytes()
    return FileSignature(
        md5=hashlib.md5(data, usedforsecurity=False).hexdigest(),
        sha1=hashlib.sha1(data, usedforsecurity=False).hexdigest(),
        sha256=hashlib.sha256(data).hexdigest(),
        size_bytes=len(data),
        file_type=detect_file_type(data),
    )


def detect_file_type(data: bytes) -> str:
    if data.startswith(b"MZ"):
        return "Windows PE executable or DLL"
    if data.startswith(b"\x7fELF"):
        return "ELF binary"
    if data.startswith(b"PK\x03\x04"):
        return "ZIP-compatible archive"
    if data.startswith(b"%PDF"):
        return "PDF document"
    if data.startswith(b"#!"):
        return "Script with shebang"
    if _looks_text(data):
        return "Text or script"
    return "Unknown binary"


def _looks_text(data: bytes) -> bool:
    if not data:
        return True
    sample = data[:4096]
    printable = sum(1 for byte in sample if byte in b"\r\n\t" or 32 <= byte <= 126)
    return printable / len(sample) > 0.85

