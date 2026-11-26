"""Stable SHA-256 fingerprints for audit reports and report files."""

import hashlib
import json
import os


def _canonical_bytes(report):
    if isinstance(report, bytes):
        return report
    if isinstance(report, str):
        return report.encode("utf-8")
    try:
        serialized = json.dumps(
            report, sort_keys=True, separators=(",", ":"),
            ensure_ascii=False, allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise TypeError("report must be UTF-8 text, bytes, or JSON-serializable data") from exc
    return serialized.encode("utf-8")


def fingerprint(report) -> str:
    """Hash text/bytes as-is, or JSON data in a key-order-independent form."""
    return hashlib.sha256(_canonical_bytes(report)).hexdigest()


def fingerprint_file(path) -> str:
    """Return the SHA-256 digest of a file, streaming large reports safely."""
    digest = hashlib.sha256()
    with open(os.fspath(path), "rb") as source:
        for chunk in iter(lambda: source.read(1024 * 64), b""):
            digest.update(chunk)
    return digest.hexdigest()
