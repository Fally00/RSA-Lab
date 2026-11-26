"""Detect RSA moduli with a cheap structural weakness (week 11)."""

import math
import time
from math import isqrt

from audit.contract import make_result
from primality.miller_rabin import miller_rabin


def _private_exponent(e, p, q, *, prime_modulus=False):
    modulus = p - 1 if prime_modulus else math.lcm(p - 1, q - 1)
    if modulus <= 1 or math.gcd(e, modulus) != 1:
        return None
    return pow(e, -1, modulus)


def _is_probable_prime(n):
    return miller_rabin(n)["is_probable_prime"]


def run(n, e):
    """Check primality, evenness, and square structure; return the audit contract."""
    start = time.perf_counter()
    if type(n) is not int or n < 2:
        raise ValueError("n must be an integer greater than or equal to 2")
    if type(e) is not int or e <= 1:
        raise ValueError("e must be an integer greater than 1")

    steps = [f"Check n = {n} for structural RSA weaknesses."]
    if n % 2 == 0:
        p, q = 2, n // 2
        steps.append(f"n is even, so 2 divides n and q = n / 2 = {q}.")
        if q == 1:
            # n=2 has no nontrivial factorization, but it is structurally invalid.
            return make_result("bad_modulus", 11, broken=True, factors=[2, 1],
                               steps=steps + ["n is the prime 2 and is not a valid RSA modulus."],
                               time_ms=(time.perf_counter() - start) * 1000)
        d = _private_exponent(e, p, q) if _is_probable_prime(q) else None
        steps.append("Recovered factors: 2 * %d = %d." % (q, n))
        if d is None:
            steps.append("A proper factor was found; a private exponent was unavailable or the cofactor is composite.")
        return make_result("bad_modulus", 11, broken=True, factors=[p, q],
                           private_key=d, steps=steps,
                           time_ms=(time.perf_counter() - start) * 1000)

    root = isqrt(n)
    if root * root == n:
        steps.append(f"n is a perfect square: n = {root}^2.")
        d = _private_exponent(e, root, root) if _is_probable_prime(root) else None
        if d is None:
            steps.append("Repeated factor found; a private exponent was unavailable or the root is composite.")
        return make_result("bad_modulus", 11, broken=True, factors=[root, root],
                           private_key=d, steps=steps,
                           time_ms=(time.perf_counter() - start) * 1000)

    primality = miller_rabin(n)
    steps.extend(primality["steps"])
    if primality["is_probable_prime"]:
        steps.append("n passed the configured Miller-Rabin bases; a prime modulus is structurally unsafe for RSA.")
        d = _private_exponent(e, n, 1, prime_modulus=True)
        if d is None:
            steps.append("The modulus is flagged, but e has no inverse modulo n - 1.")
        return make_result("bad_modulus", 11, broken=True, factors=[n, 1],
                           private_key=d, steps=steps,
                           time_ms=(time.perf_counter() - start) * 1000)

    steps.append("n is odd, composite, and not a perfect square; no structural flaw was detected by this check.")
    return make_result("bad_modulus", 11, steps=steps,
                       time_ms=(time.perf_counter() - start) * 1000)
