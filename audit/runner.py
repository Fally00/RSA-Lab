"""
audit/runner.py
Owner: Rayan
Purpose: Call every registered attack on each key and merge the results into one report.
"""
from attacks import ATTACK_REGISTRY, SINGLE_ATTACKS
from attacks.shared_prime import run_batch
from audit.contract import jsonify as serialize_result, verdict
from audit.parser import parse_keys
from report.fingerprint import fingerprint


def audit_key(n: int, e: int, label: str = "key-1") -> dict:
    """Run all single-key attacks on (n, e) and return a serialized key audit entry."""
    raw_results = [fn(n, e) for _, _, fn in SINGLE_ATTACKS]
    status = "BROKEN" if any(r.get("broken") for r in raw_results) else "SAFE"
    return {
        "label": label,
        "n": str(n),
        "e": str(e),
        "bits": n.bit_length(),
        "verdict": status,
        "results": [serialize_result(r) for r in raw_results],
    }


def run_audit(raw_input: str) -> dict:
    """Parse input keys, run all single + batch attacks, and fingerprint the report."""
    parsed_keys = parse_keys(raw_input)
    key_entries = [audit_key(k["n"], k["e"], k["label"]) for k in parsed_keys]

    batch_raw = run_batch(parsed_keys)
    batch_results = [serialize_result(r) for r in batch_raw]

    # Attach each key's batch result to its per-key results list and update verdict if broken.
    for entry, b_res in zip(key_entries, batch_results):
        entry["results"].append(b_res)
        if b_res.get("broken"):
            entry["verdict"] = "BROKEN"

    report_hash = fingerprint({"keys": key_entries, "batch": batch_results})
    return {
        "schema_version": 1,
        "attack_registry": ATTACK_REGISTRY,
        "keys": key_entries,
        "batch": batch_results,
        "report": {
            "sha256": report_hash,
            "covers": "keys",
            "week": 13,
        },
    }


