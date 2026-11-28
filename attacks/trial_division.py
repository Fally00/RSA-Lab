"""
attacks/trial_division.py
Owner: Member 3
Purpose: W3: try small divisors up to sqrt(n).
Follows the shared contract: run(n, e) -> dict (see README section 7).
"""
import time
from math import isqrt

import config
from audit.contract import make_result, elapsed_time, derive_private_key, table


def run(n, e, limit=None):
    """Trial division attack on an RSA modulus, returning a contract dict."""
    start = time.perf_counter()
    max_limit = limit if limit is not None else config.TRAIL_DIVISION_LIMIT
    bound = min(isqrt(n), max_limit)

    steps = [
        f"Divide n by 2, then every odd d up to {bound}. A hit means d | n (W1 divisibility, W3 primes)."
    ]
    rows = []

    if n % 2 == 0:
        rows.append(["2", "0"])
        p, q = 2, n // 2
    else:
        rows.append(["2", str(n % 2)])
        p = q = None
        candidates = 1
        for divisor in range(3, bound + 1, 2):
            rem = n % divisor
            if len(rows) < 6 or rem == 0:
                rows.append([str(divisor), str(rem)])
            candidates += 1
            if rem == 0:
                p, q = divisor, n // divisor
                break

    steps.append(table(["d", "n mod d"], rows))

    if p is None or p == q or p <= 1 or q <= 1:
        steps.append(f"No non-trivial divisor found up to {bound}. Smallest prime factor is larger than that.")
        return make_result("trial_division", 3, broken=False, steps=steps, time_ms=elapsed_time(start))

    d = derive_private_key(e, p, q)
    steps.append(f"d = {p} divides n, so q = n / d = {q}.")
    steps.append(f"n = {p} x {q}")

    return make_result(
        "trial_division",
        3,
        broken=True,
        factors=[p, q],
        private_key=d,
        steps=steps,
        time_ms=elapsed_time(start),
    )


if __name__ == "__main__":
    print("Trial Division Attack - enter the RSA public key\n")
    try:
        n = int(input("Enter n (modulus): ").strip())
        e = int(input("Enter e (public exponent): ").strip())
    except ValueError:
        print("[-] n and e must be whole numbers.")
        raise SystemExit(1)

    print()
    res = run(n, e)
    print(res)
