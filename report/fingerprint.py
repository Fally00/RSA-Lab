"""
report/fingerprint.py
Owner: Member 6
Purpose: W13: SHA-256 fingerprint of each audit report.
"""
import hashlib
import json



def fingerprint(report) -> str:

    if isinstance(report, dict):        
        report = json.dumps(report, sort_keys=True, separators=(",", ":"))
    if isinstance(report, str):
        report = report.encode("utf-8")
    return hashlib.sha256(report).hexdigest()


def fingerprint_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


if __name__ == "__main__":
    keys = int(input("Enter Keys: "))
    weak = int(input("Enter Weak: "))

    report = {
        "keys": keys,
        "weak": weak,
    }

    result = fingerprint(report)

    print("\nAudit Report:", report)
    print(" Fingerprint:", result)


