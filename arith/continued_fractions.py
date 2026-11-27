from __future__ import annotations

import math
from typing import Iterable


def cf_expansion_fraction(num: int, den: int) -> list[int]:
    """Expand a rational number num / den into simple continued fraction terms."""
    if den == 0:
        raise ZeroDivisionError("Denominator cannot be zero.")
    if den < 0:
        num, den = -num, -den

    coeffs: list[int] = []
    while den != 0:
        q = num // den
        coeffs.append(q)
        num, den = den, num - q * den
    return coeffs


def cf_expansion_float(x: float, max_terms: int = 25, tol: float = 1e-12) -> list[int]:
    """Expand a real number x into simple continued fraction terms."""
    if math.isnan(x) or math.isinf(x):
        raise ValueError("Value must be finite.")

    coeffs: list[int] = []
    val = x
    for _ in range(max_terms):
        a = math.floor(val)
        coeffs.append(a)
        rem = val - a
        if abs(rem) < tol:
            break
        val = 1.0 / rem
    return coeffs


def convergents(coeffs: Iterable[int]) -> list[tuple[int, int]]:
    """Compute convergents (numerator, denominator) from continued fraction terms."""
    p_prev2, p_prev1 = 0, 1
    q_prev2, q_prev1 = 1, 0
    result: list[tuple[int, int]] = []

    for a in coeffs:
        p = a * p_prev1 + p_prev2
        q = a * q_prev1 + q_prev2
        result.append((p, q))
        p_prev2, p_prev1 = p_prev1, p
        q_prev2, q_prev1 = q_prev1, q

    return result
