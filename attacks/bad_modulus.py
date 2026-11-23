"""
attacks/bad_modulus.py
Owner: Member 5(Haneen)
Purpose: W11: flag n that is prime, a perfect square, or even.
Follows the shared contract: run(n, e) -> dict (see README section 7).
"""

import time
from math import isqrt

from core.modular import modinv
from primality import miller_rabin


def run(n, e):
    start_time = time.perf_counter()
    steps = [f"Starting bad modulus check for n = {n}."]

    if not isinstance(n, int) or isinstance(n, bool) or n < 2:
        raise ValueError("n must be an integer greater than or equal to 2.")

    if not isinstance(e, int) or isinstance(e, bool) or e <= 0:
        raise ValueError("e must be a positive integer.")

    result = {
        "attack": "bad_modulus",
        "week": 11,
        "broken": False,
        "factors": None,
        "private_key": None,
        "steps": steps,
        "time_ms": 0.0
    }

    def finish():
        result["time_ms"] = (time.perf_counter() - start_time) * 1000
        return result

    is_prime = miller_rabin(n)["is_probable_prime"]

    if is_prime:
        steps.append("n is prime. phi(n) = n - 1.")
        result["broken"] = True
        result["factors"] = [n, 1]
        phi = n - 1

        try:
            result["private_key"] = modinv(e, phi)
        except ValueError:
            steps.append("Could not compute private key (e not coprime with phi).")

        return finish()

    if n % 2 == 0:
        steps.append("n is even.")
        p, q = 2, n // 2
        result["broken"] = True
        result["factors"] = [p, q]
        phi = (p - 1) * (q - 1)

        try:
            result["private_key"] = modinv(e, phi)
        except ValueError:
            steps.append("Could not compute private key (e not coprime with phi).")

        return finish()

    root = isqrt(n)

    if root * root == n:
        steps.append("n is a perfect square (p = q).")
        p = q = root
        result["broken"] = True
        result["factors"] = [p, q]
        phi = p * (p - 1)

        try:
            result["private_key"] = modinv(e, phi)
        except ValueError:
            steps.append("Could not compute private key (e not coprime with phi).")

        return finish()

    steps.append(
        "n is odd, composite, and not a perfect square. Bad modulus attack failed."
    )

    return finish()