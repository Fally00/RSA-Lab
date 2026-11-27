"""
attacks/wiener.py
Owner: Member 4
Purpose: W5: small-d attack using continued fractions; put the convergents table in steps.
Follows the shared contract: run(n, e) -> dict (see README section 7).
"""
import time
from math import isqrt

from arith.continued_fractions import cf_expansion_fraction, convergents
from audit.contract import make_result, elapsed_time, derive_private_key, table


def is_perfect_square(x):
    if x < 0:
        return False, 0
    r = isqrt(x)
    return r * r == x, r


def try_candidate(n, e, k, d):
    """Build phi(n), solve the quadratic, check p, q are factors."""
    if k == 0 or d <= 0:
        return None, False, None, False

    if (e * d - 1) % k != 0:
        return None, False, None, False
    phi = (e * d - 1) // k
    if phi <= 0:
        return None, True, phi, False

    b = n - phi + 1
    discriminant = b * b - 4 * n
    is_sq, sqrt_disc = is_perfect_square(discriminant)
    if not is_sq:
        return None, True, phi, False

    if (b - sqrt_disc) % 2 != 0:
        return None, True, phi, True

    p = (b - sqrt_disc) // 2
    q = (b + sqrt_disc) // 2

    if p * q == n and p > 1 and q > 1 and p != q:
        return (p, q, d), True, phi, True
    return None, True, phi, True


def run(n, e):
    """Full Wiener attack pipeline returning a contract dict."""
    start = time.perf_counter()
    cf = cf_expansion_fraction(e, n)
    convs = convergents(cf)

    cf_preview = str(cf[:8])[:-1] + ", ...]" if len(cf) > 8 else str(cf)
    steps = [
        "If d < n^(1/4)/3 then k/d is a convergent of the continued fraction of e/n. For each convergent k/d: phi = (e*d - 1)/k, then solve x^2 - (n - phi + 1)x + n = 0 (W5, W7).",
        f"Continued fraction of e/n starts {cf_preview}",
    ]

    rows = []
    found = None
    for i, (k, d) in enumerate(convs):
        if k == 0:
            continue
        res, divisible, phi_cand, disc_sq = try_candidate(n, e, k, d)
        if len(rows) < 15 or res is not None:
            rows.append([
                str(i),
                f"{k}/{d}",
                "yes" if divisible else "no",
                str(phi_cand) if divisible else "-",
                ("yes" if disc_sq else "no") if divisible else "-",
            ])
        if res is not None:
            found = res
            break

    steps.append(table(["i", "k/d", "k | e*d-1 ?", "phi candidate", "disc square?"], rows))

    if found is not None:
        p, q, d_found = found
        priv = derive_private_key(e, p, q) or d_found
        steps.append(f"Convergent yields valid phi. n = {p} x {q}")
        return make_result(
            "wiener",
            5,
            broken=True,
            factors=[p, q],
            private_key=priv,
            steps=steps,
            time_ms=elapsed_time(start),
        )

    steps.append("No convergent gives a valid phi. d is not small enough for Wiener.")
    return make_result("wiener", 5, broken=False, steps=steps, time_ms=elapsed_time(start))


if __name__ == "__main__":
    try:
        n = int(input("Enter n (modulus): ").strip())
        e = int(input("Enter e (public exponent): ").strip())
    except ValueError:
        print("Invalid input: n and e must be integers.")
        raise SystemExit(1)

    print(run(n, e))
