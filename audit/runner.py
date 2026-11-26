"""Run the registered RSA attacks and assemble the audit API response."""

from contextlib import redirect_stdout
import io
import math
import time

from attacks import ATTACKS
from audit.contract import derive_private_key, jsonify, make_result, validate, verdict
from audit.parser import parse_key
from report.fingerprint import fingerprint


def _key_pair(key):
    if isinstance(key, (tuple, list)) and len(key) == 2:
        n, e = key
        if type(n) is not int or type(e) is not int:
            raise ValueError("n and e must be integers")
        if n <= 1 or e <= 1:
            raise ValueError("n and e must both be greater than 1")
        return n, e
    return parse_key(key)


def _failed(name, week, message, elapsed):
    return make_result(name, week, steps=[message], time_ms=elapsed)


def _coerce_result(name, week, raw, elapsed, n, e):
    """Adapt older teaching attacks to the common result-dictionary contract."""
    if isinstance(raw, dict) and all(k in raw for k in
                                     ("attack", "week", "broken", "factors", "private_key", "steps", "time_ms")):
        result = dict(raw)
        result["time_ms"] = elapsed if result["time_ms"] is None else result["time_ms"]
        validate(result)
        if result["broken"] and not _verified(n, e, result):
            return _failed(name, week, "The attack returned a factorization that failed verification.", elapsed)
        return result

    p = q = d = None
    steps = []
    if isinstance(raw, dict):
        p, q = raw.get("p"), raw.get("q")
        d = raw.get("d")
        raw_steps = raw.get("steps", [])
        steps = [f"Tried divisor {item[0]}: {'found' if item[1] else 'not a factor'}."
                 for item in raw_steps if isinstance(item, (tuple, list)) and len(item) == 2]
        if p is not None and q is not None:
            steps.append(f"Recovered factors {p} and {q}.")
    elif isinstance(raw, (tuple, list)) and len(raw) >= 2:
        p, q = raw[0], raw[1]
        d = raw[2] if len(raw) > 2 else None
        steps.append(f"Recovered candidate factors {p} and {q}.")

    if type(p) is int and type(q) is int and p * q == n and p > 1 and q > 1:
        if d is None:
            d = derive_private_key(e, p, q)
        result = make_result(name, week, broken=True, factors=[p, q], private_key=d,
                             steps=steps or ["A factorization was recovered."], time_ms=elapsed)
        try:
            validate(result)
        except (ValueError, TypeError):
            return _failed(name, week, "Recovered factors could not be represented by the shared contract.", elapsed)
        if _verified(n, e, result):
            return result
        return _failed(name, week, "The attack result failed factor or private-exponent verification.", elapsed)

    return make_result(name, week, steps=steps or ["No factorization was found."], time_ms=elapsed)


def _verified(n, e, result):
    if not result["broken"]:
        return True
    p, q = result["factors"]
    if p * q != n:
        return False
    d = result["private_key"]
    if d is None:
        return True
    if p == 1 or q == 1:
        modulus = max(p, q) - 1
    elif p == q:
        modulus = p * (p - 1)
    else:
        modulus = math.lcm(p - 1, q - 1)
    return modulus > 0 and (d * e) % modulus == 1


def _run_one(entry, n, e):
    start = time.perf_counter()
    captured = io.StringIO()
    try:
        with redirect_stdout(captured):
            raw = entry["module"].run(n, e)
        elapsed = (time.perf_counter() - start) * 1000
        return _coerce_result(entry["name"], entry["week"], raw, elapsed, n, e)
    except Exception as exc:
        elapsed = (time.perf_counter() - start) * 1000
        return _failed(entry["name"], entry["week"],
                       f"Attack could not complete: {type(exc).__name__}: {exc}", elapsed)


def _as_json_result(result):
    return jsonify(result)


def run_audit(keys):
    """Audit a sequence of ``(n, e)`` pairs or raw public-key objects.

    Returns the same top-level shape consumed by the frontend and illustrated
    by ``docs/mock_results.json``. Big integers are serialized as decimal text.
    """
    if isinstance(keys, dict) or isinstance(keys, str):
        keys = [keys]
    elif isinstance(keys, tuple) and len(keys) == 2 and all(type(x) is int for x in keys):
        keys = [keys]
    parsed = [_key_pair(key) for key in keys]
    prepared = [{"n": n, "e": e} for n, e in parsed]
    key_results = []
    batch_results = []

    for index, (n, e) in enumerate(parsed, start=1):
        results = [_run_one(entry, n, e) for entry in ATTACKS if not entry["batch"]]
        key_results.append({
            "label": f"key-{index}",
            "n": str(n),
            "e": str(e),
            "bits": n.bit_length(),
            "verdict": verdict(results).upper(),
            "results": [_as_json_result(result) for result in results],
        })

    shared_entry = next((entry for entry in ATTACKS if entry["batch"]), None)
    if shared_entry is not None:
        try:
            batch_results = shared_entry["module"].run_batch(prepared)
        except Exception as exc:
            batch_results = [
                _failed(shared_entry["name"], shared_entry["week"],
                        f"Batch attack could not complete: {type(exc).__name__}: {exc}", 0.0)
                for _ in parsed
            ]
        for key, result in zip(key_results, batch_results):
            try:
                validate(result)
                key["results"].append(_as_json_result(result))
                if result["broken"]:
                    key["verdict"] = "BROKEN"
            except (ValueError, TypeError):
                fallback = _failed(shared_entry["name"], shared_entry["week"],
                                   "Batch result failed contract validation.", 0.0)
                key["results"].append(_as_json_result(fallback))
        batch_results = [_as_json_result(result) for result in batch_results]

    body = {
        "schema_version": 1,
        "attack_registry": [
            {"attack": entry["name"], "week": entry["week"], "batch": entry["batch"]}
            for entry in ATTACKS
        ],
        "keys": key_results,
        "batch": batch_results,
    }
    body["report"] = {"sha256": fingerprint(body), "covers": "keys", "week": 13}
    return body


def run(keys):
    """Compatibility alias for callers that refer to the runner as ``run``."""
    return run_audit(keys)


__all__ = ["run", "run_audit"]
