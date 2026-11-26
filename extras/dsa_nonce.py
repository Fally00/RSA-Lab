"""Recover a DSA private key when the same nonce signs two messages.

Each signature is supplied as ``(z, r, s)``, where ``z`` is the integer
message digest used by DSA. Given subgroup order q:

    k = (z1 - z2) / (s1 - s2) mod q
    x = (s1*k - z1) / r mod q

These helpers are standalone educational utilities; they are not wired into
the RSA audit runner.
"""


def _signature(value, q):
    if not isinstance(value, (tuple, list)) or len(value) != 3:
        raise ValueError("each signature must be a (z, r, s) triple")
    z, r, s = value
    if any(type(item) is not int for item in value):
        raise ValueError("signature values must be integers")
    if not 1 <= r < q or not 1 <= s < q:
        raise ValueError("signature r and s must be in the range 1..q-1")
    return z % q, r, s


def recover_reused_nonce(q, signature1, signature2):
    """Return ``(k, x)`` from two DSA signatures that reused one nonce."""
    if type(q) is not int or q <= 2:
        raise ValueError("q must be an integer greater than 2")
    z1, r1, s1 = _signature(signature1, q)
    z2, r2, s2 = _signature(signature2, q)
    if r1 != r2:
        raise ValueError("the signatures do not have the same r; nonce reuse is not established")
    denominator = (s1 - s2) % q
    if denominator == 0:
        raise ValueError("s1 - s2 is not invertible modulo q")
    k = ((z1 - z2) * pow(denominator, -1, q)) % q
    if k == 0:
        raise ValueError("recovered nonce is zero, so the signatures are invalid")
    x = ((s1 * k - z1) * pow(r1, -1, q)) % q
    if x == 0:
        raise ValueError("recovered private key is zero, so the signatures are invalid")
    if (s1 * k - z1 - x * r1) % q or (s2 * k - z2 - x * r2) % q:
        raise ValueError("signatures are inconsistent with a reused nonce")
    return k, x


def recover_private_key(q, signature1, signature2, *, p=None, g=None, y=None):
    """Recover the private scalar; optionally verify it against public key y."""
    _nonce, private_key = recover_reused_nonce(q, signature1, signature2)
    if any(value is not None for value in (p, g, y)):
        if any(type(value) is not int for value in (p, g, y)):
            raise ValueError("provide p, g, and y together as integers to verify the key")
        if p <= 2 or not 1 < g < p or not 0 < y < p:
            raise ValueError("invalid DSA public parameters")
        if pow(g, private_key, p) != y:
            raise ValueError("recovered scalar does not match public key y")
    return private_key
