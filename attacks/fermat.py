"""
attacks/fermat.py
Owner: Member 3
Purpose: W12: Fermat factorization (works when p and q are close).
Follows the shared contract: run(n, e) -> dict (see README section 7).
"""
import time
from math import isqrt

import config
from audit.contract import make_result, elapsed_time, derive_private_key, table


def is_perfect_square(x):
    """Return (True, root) if x is a perfect square, else (False, None)."""
    if x < 0:
        return False, None
    r = isqrt(x)
    return (r * r == x), r


def run(n, e, max_steps=None):
    """Fermat factorization attack returning a contract dict."""
    start = time.perf_counter()
    limit = max_steps if max_steps is not None else config.FERMAT_LIMIT

    steps = [
        "If p and q are close, n = a^2 - b^2 with a = (p+q)/2 near sqrt(n). Try a = ceil(sqrt n), a+1, ... until a^2 - n is a perfect square (W12)."
    ]
    rows = []

    if n % 2 == 0:
        p, q = 2, n // 2
        steps.append(f"n is even -> 2 is a factor: n = {p} x {q}")
    else:
        a = isqrt(n)
        if a * a < n:
            a += 1

        p = q = None
        for step_idx in range(1, limit + 1):
            b2 = a * a - n
            ok, b = is_perfect_square(b2)
            if len(rows) < 6 or ok:
                rows.append([str(step_idx), str(a), str(b2), "yes" if ok else "no"])
            if ok:
                p, q = a - b, a + b
                steps.append(table(["iter", "a", "a^2 - n", "square?"], rows))
                steps.append(f"b = {b}, so p = a - b, q = a + b.")
                break
            a += 1

        if p is None:
            steps.append(table(["iter", "a", "a^2 - n", "square?"], rows))
            steps.append(f"No square found in {limit} iterations: p and q are not close enough.")
            return make_result("fermat", 12, broken=False, steps=steps, time_ms=elapsed_time(start))

    if p <= 1 or q <= 1 or p == q or p * q != n:
        steps.append("Recovered values do not form two distinct factors > 1.")
        return make_result("fermat", 12, broken=False, steps=steps, time_ms=elapsed_time(start))

    d = derive_private_key(e, p, q)
    steps.append(f"n = {p} x {q}")

    return make_result(
        "fermat",
        12,
        broken=True,
        factors=[p, q],
        private_key=d,
        steps=steps,
        time_ms=elapsed_time(start),
    )


def ask_int(message, optional=False):
    """Ask the user for an integer until a valid one is entered."""
    while True:
        value = input(message).strip()
        if optional and value == "":
            return None
        try:
            return int(value)
        except ValueError:
            print("  Please enter a valid whole number.")


if __name__ == "__main__":
    print("=" * 50)
    print("        Fermat Factorization Attack on RSA")
    print("=" * 50)
    n = ask_int("Enter n (modulus): ")
    e = ask_int("Enter e (public exponent, usually 65537): ")
    print(run(n, e))
