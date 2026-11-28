from __future__ import annotations

import math


def _factorize(n: int) -> dict[int, int]:
    """Return prime factorization {prime: exponent} for positive integer n."""
    if n < 1:
        raise ValueError("n must be a positive integer.")
    factors: dict[int, int] = {}
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2
    d = 3
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def tau(n: int) -> int:
    """Number of positive divisors of n, denoted tau(n) or d(n)."""
    factors = _factorize(n)
    count = 1
    for exp in factors.values():
        count *= (exp + 1)
    return count


def sigma(n: int, k: int = 1) -> int:
    """Sum of k-th powers of positive divisors of n; default k=1 gives sigma(n)."""
    if k < 0:
        raise ValueError("k must be non-negative.")
    factors = _factorize(n)
    total = 1
    for p, exp in factors.items():
        if k == 0:
            total *= (exp + 1)
        else:
            p_k = p ** k
            total *= (p_k ** (exp + 1) - 1) // (p_k - 1)
    return total


def aliquot_sum(n: int) -> int:
    """Sum of proper positive divisors of n: s(n) = sigma(n) - n."""
    if n < 1:
        raise ValueError("n must be a positive integer.")
    return sigma(n, 1) - n


def is_perfect(n: int) -> bool:
    """Return True if n > 0 equals the sum of its proper divisors."""
    return n > 0 and aliquot_sum(n) == n
