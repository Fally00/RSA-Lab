"""Parse one RSA public key from PEM, JSON, a mapping, or raw ``n, e`` text."""

import json
import re


_PAIR = re.compile(
    r"^\s*(?:n\s*[:=]\s*)?(\d+)\s*[,;\s]+(?:e\s*[:=]\s*)?(\d+)\s*$",
    re.IGNORECASE,
)


def _validate(n, e):
    if type(n) is not int or type(e) is not int:
        raise ValueError("n and e must be integers")
    if n <= 1 or e <= 1:
        raise ValueError("modulus n and public exponent e must be greater than 1")
    return n, e


def _integer(value):
    if type(value) is int:
        return value
    if isinstance(value, str) and re.fullmatch(r"\d+", value.strip()):
        return int(value)
    raise ValueError("value is not a decimal integer")


def parse_key(data):
    """Return an ``(n, e)`` pair for an RSA public key.

    PEM input is loaded with the project's sole cryptography dependency. Raw
    text accepts either ``n, e`` or ``n=<decimal>, e=<decimal>``.
    """
    if isinstance(data, dict):
        if "n" not in data or "e" not in data:
            raise ValueError("public key must contain 'n' and 'e' fields")
        try:
            return _validate(_integer(data["n"]), _integer(data["e"]))
        except (TypeError, ValueError) as exc:
            raise ValueError("n and e must be decimal integers") from exc

    if not isinstance(data, str):
        raise ValueError("public key must be PEM text, raw n/e text, or a dictionary")
    text = data.strip()
    if not text:
        raise ValueError("public key input is empty")

    if text.startswith("-----BEGIN"):
        try:
            from cryptography.hazmat.primitives import serialization
            from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
            public_key = serialization.load_pem_public_key(text.encode("ascii"))
        except (ImportError, ValueError, TypeError, UnicodeEncodeError) as exc:
            raise ValueError("invalid or unsupported PEM public key") from exc
        if not isinstance(public_key, RSAPublicKey):
            raise ValueError("PEM key must be an RSA public key")
        numbers = public_key.public_numbers()
        return _validate(numbers.n, numbers.e)

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = _PAIR.fullmatch(text)
        if match:
            return _validate(int(match.group(1)), int(match.group(2)))
        raise ValueError("expected JSON with n/e fields, raw 'n, e', or an RSA public PEM")

    if not isinstance(data, dict) or "n" not in data or "e" not in data:
        raise ValueError("public key JSON must be an object containing n and e")
    try:
        return _validate(_integer(data["n"]), _integer(data["e"]))
    except (TypeError, ValueError) as exc:
        raise ValueError("n and e must be decimal integers") from exc
