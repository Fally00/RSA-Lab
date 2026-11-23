
"""
attacks/phi_leak.py
Owner: Rayan
Purpose: Recover RSA factors using leaked phi(n) or sigma(n).
"""

import math
import sys
import time
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from audit.contract import make_result, elapsed_time, derive_private_key, table

def run(n, e, phi=None, sigma=None):
    start = time.perf_counter()
    steps = []

    # Validate inputs
    if type(n) is not int or n <= 1:
        raise ValueError("n must be a positive integer greater than 1")
    
    # If phi(n) is provided, compute the factors p and q.
    if phi is not None and sigma is None:
        return make_result(
            "phi_leak", 6,
            steps=["No phi(n) or sigma(n) value was provided."],
            time_ms=elapsed_time(start)
        )

    # Validate leaked values
    if phi is not None and (type(phi) is not int or phi <= 0):
        raise ValueError("phi must be a positive integer")

    if sigma is not None and (type(sigma) is not int or sigma <= 0):
        raise ValueError("sigma must be a positive integer")

    if phi is not None:
        S = n - phi + 1
        week = 6
        steps.append(f"Using phi(n): p + q = n - phi(n) + 1 = {S}")

    else:
        S = sigma - n - 1
        week = 7
        steps.append(f"Using sigma(n): p + q = sigma(n) - n - 1 = {S}")

    if phi is not None and sigma is not None:
        sigma_sum = sigma - n - 1

        if S != sigma_sum:
            raise ValueError("The supplied phi and sigma values are inconsistent")

        steps.append("Both leaked values produce the same p + q.")

    delta = S**2 - 4*n
    steps.append(f"Discriminant: delta = S^2 - 4n = {delta}")

    if delta < 0:
        return make_result(
            "phi_leak", week,
            steps=steps + ["Discriminant is negative, no real roots exist."],
            time_ms=elapsed_time(start)
        )
    root = math.isqrt(delta)
    
    if root**2 != delta:
            steps.append("Discriminant is not a perfect square.")
            return make_result(
                "phi_leak", week,
                steps=steps,
                time_ms=elapsed_time(start)
            )
    
        # Recover p and q
    if (S + root) % 2 != 0 or (S - root) % 2 != 0:
            steps.append("The resulting roots are not integers.")
            return make_result(
                "phi_leak", week,
                steps=steps,
                time_ms=elapsed_time(start)
            )
    
    p = (S + root) // 2
    q = (S - root) // 2

    if p <= 1 or q <= 1 or p == q or p * q != n:
            steps.append("Recovered values do not form a valid factorization.")
            return make_result(
                "phi_leak", week,
                steps=steps,
                time_ms=elapsed_time(start)
            )
    
    steps.append(f"Recovered factors: p = {p}, q = {q}")

    # Derive the private exponent if possible
    d = derive_private_key(e, p, q)

    if d is not None:
        steps.append(f"Recovered private exponent: d = {d}")
    else:
        steps.append("Factors recovered, but the private exponent could not be derived.")

    return make_result(
        "phi_leak",
        week,
        broken=True,
        factors=[p, q],
        private_key=d,
        steps=steps,
        time_ms=elapsed_time(start)
    ) 