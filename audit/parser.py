"""
audit/parser.py
Owner: Rayan
Purpose: Turn PEM public keys and raw 'n, e' text into (n, e) pairs.
"""

import json
import re

import config


def parse_key(data):
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")

    if not isinstance(data, dict):
        raise ValueError("Public key must be a dictionary")

    if "n" not in data or "e" not in data:
        raise ValueError("Public key must contain 'n' and 'e' fields")

    n = int(data["n"]) if isinstance(data["n"], str) and data["n"].strip().isdigit() else data["n"]
    e = int(data["e"]) if isinstance(data["e"], str) and data["e"].strip().isdigit() else data["e"]

    if type(n) is not int or type(e) is not int:
        raise ValueError("n and e must be integers")

    if n <= 1 or e <= 1:
        raise ValueError("Modulus n and public exponent e must be greater than 1")

    if n.bit_length() > config.MAX_MODULUS:
        raise ValueError(f"Modulus exceeds MAX_MODULUS ({config.MAX_MODULUS} bits)")

    return n, e


def _parse_pem_block(pem_text):
    try:
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
        from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
    except ImportError as exc:
        raise ValueError("PEM parsing requires the 'cryptography' package.") from exc

    key = load_pem_public_key(pem_text.encode("utf-8"))
    if not isinstance(key, RSAPublicKey):
        raise ValueError("PEM key is not an RSA public key.")
    nums = key.public_numbers()
    return parse_key({"n": nums.n, "e": nums.e})


def parse_keys(raw_input):
    """Parse JSON, PEM block(s), or line-based 'n, e' text into a list of key dicts."""
    if not isinstance(raw_input, str) or not raw_input.strip():
        raise ValueError("Input must be a non-empty string.")

    text = raw_input.strip()
    keys = []

    if text.startswith("{") or text.startswith("["):
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON format") from exc
        items = parsed if isinstance(parsed, list) else [parsed]
        for idx, item in enumerate(items):
            n, e = parse_key(item)
            label = item.get("label", f"key-{idx + 1}") if isinstance(item, dict) else f"key-{idx + 1}"
            keys.append({"label": label, "n": n, "e": e})
    elif "-----BEGIN " in text:
        pem_blocks = re.findall(
            r"-----BEGIN [A-Z ]+-----.*?-----END [A-Z ]+-----",
            text,
            flags=re.DOTALL,
        )
        if not pem_blocks:
            raise ValueError("Invalid PEM block.")
        for idx, block in enumerate(pem_blocks):
            n, e = _parse_pem_block(block)
            keys.append({"label": f"key-{idx + 1}", "n": n, "e": e})
    else:
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            label = None
            if ":" in line:
                label_part, line = line.split(":", 1)
                label = label_part.strip()
                line = line.strip()
            parts = [p for p in re.split(r"[\s,]+", line) if p]
            if len(parts) != 2:
                raise ValueError(f"Expected 'n, e' pair, got: {line}")
            try:
                n = int(parts[0], 0)
                e = int(parts[1], 0)
            except ValueError as exc:
                raise ValueError(f"Invalid integer in line: {line}") from exc
            n, e = parse_key({"n": n, "e": e})
            keys.append({"label": label or f"key-{len(keys) + 1}", "n": n, "e": e})

    if not keys:
        raise ValueError("No valid keys found in input.")
    if len(keys) > config.MAX_KEYS:
        raise ValueError(f"Too many keys (max {config.MAX_KEYS}).")
    return keys