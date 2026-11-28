"""
attacks/pollard_rho.py
Owner: Member 3
Purpose: W12: Pollard's rho factoring.
Follows the shared contract: run(n, e) -> dict (see README section 7).
"""
import time
from math import gcd

import config
from audit.contract import make_result, elapsed_time, derive_private_key, table


MAX_C_RETRIES = 20


def f(x, c, n):
    """The pseudo-random function: f(x) = x^2 + c mod n"""
    return (x * x + c) % n


def run(n, e, max_iter=None):
    """Factor n with Pollard's rho, returning a contract dict."""
    start = time.perf_counter()
    limit = max_iter if max_iter is not None else config.POLLARD_RHO_MAX_ITER

    steps = [
        "Walk x -> x^2 + c (mod n) with a tortoise and a hare. When the walks collide mod a hidden prime p, gcd(|x - y|, n) reveals p (W12, W10 cost ~ sqrt(p))."
    ]
    rows = []

    if n % 2 == 0:
        p = 2
    else:
        p = None
        c = 1
        while p is None and c <= MAX_C_RETRIES:
            x, y, d = 2, 2, 1
            iters = 0
            c_rows = []
            while d == 1 and iters < limit:
                x = f(x, c, n)
                y = f(f(y, c, n), c, n)
                d = gcd(abs(x - y), n)
                iters += 1
                if len(c_rows) < 5 or d > 1:
                    c_rows.append([str(iters), str(x), str(y), str(d)])
            if 1 < d < n:
                p = d
                steps.append(f"c = {c}")
                steps.append(table(["i", "x", "y", "gcd(|x-y|, n)"], c_rows))
                steps.append(f"gcd = {p} is a proper factor after {iters} iterations.")
            else:
                c += 1

    if p is None or p <= 1 or n // p <= 1 or p == n // p:
        steps.append(f"No factor found in {limit} iterations per attempt.")
        return make_result("pollard_rho", 12, broken=False, steps=steps, time_ms=elapsed_time(start))

    q = n // p
    priv_d = derive_private_key(e, p, q)
    steps.append(f"n = {p} x {q}")

    return make_result(
        "pollard_rho",
        12,
        broken=True,
        factors=[p, q],
        private_key=priv_d,
        steps=steps,
        time_ms=elapsed_time(start),
    )


def main():
    print("=== Pollard's Rho Attack on RSA ===")
    try:
        n = int(input("Step 1 - Enter the modulus n (positive integer): "))
        e = int(input("Step 2 - Enter the public exponent e (e.g. 65537): "))
    except ValueError:
        print("Error: please enter whole numbers only.")
        return
    print(run(n, e))


if __name__ == "__main__":
    main()
