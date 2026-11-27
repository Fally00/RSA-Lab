from __future__ import annotations

import math


def sqrt_continued_fraction_period(d: int) -> tuple[int, list[int]]:
    """Return (a0, periodic_part) for continued fraction of sqrt(d) for non-square d > 0."""
    if d <= 0:
        raise ValueError("d must be a positive integer.")
    a0 = math.isqrt(d)
    if a0 * a0 == d:
        raise ValueError("d must not be a perfect square.")

    m = 0
    denom = 1
    a = a0
    period: list[int] = []

    while True:
        m = denom * a - m
        denom = (d - m * m) // denom
        a = (a0 + m) // denom
        period.append(a)
        if a == 2 * a0:
            break

    return a0, period


def fundamental_pell_solution(d: int) -> tuple[int, int]:
    """Find smallest positive integer solution (x, y) to x^2 - d*y^2 = 1."""
    a0, period = sqrt_continued_fraction_period(d)
    h_prev2, h_prev1 = 0, 1
    k_prev2, k_prev1 = 1, 0

    coeffs = [a0]
    idx = 0
    while True:
        if idx > 0:
            coeffs.append(period[(idx - 1) % len(period)])
        a = coeffs[-1]
        h = a * h_prev1 + h_prev2
        k = a * k_prev1 + k_prev2
        if h * h - d * k * k == 1:
            return h, k
        h_prev2, h_prev1 = h_prev1, h
        k_prev2, k_prev1 = k_prev1, k
        idx += 1


def pell_solutions(d: int, count: int = 5) -> list[tuple[int, int]]:
    """Generate first `count` positive integer solutions (x, y) to x^2 - d*y^2 = 1."""
    if count < 1:
        return []
    x1, y1 = fundamental_pell_solution(d)
    sols: list[tuple[int, int]] = [(x1, y1)]
    xk, yk = x1, y1
    for _ in range(1, count):
        xk, yk = x1 * xk + d * y1 * yk, x1 * yk + y1 * xk
        sols.append((xk, yk))
    return sols
