from __future__ import annotations

import math

from arith.arith_functions import _factorize as factorize


def euler_phi(n: int) -> int:
    """Euler's totient function phi(n) for positive integer n."""
    factors = factorize(n)
    result = n
    for p in factors:
        result = result // p * (p - 1)
    return result


def carmichael_lambda(n: int) -> int:
    """Carmichael function lambda(n): smallest m >= 1 with a^m = 1 (mod n) for all gcd(a, n)=1."""
    if n < 1:
        raise ValueError("n must be a positive integer.")
    factors = factorize(n)
    lam = 1
    for p, exp in factors.items():
        if p == 2 and exp >= 3:
            term = 1 << (exp - 2)
        else:
            term = (p ** (exp - 1)) * (p - 1)
        lam = math.lcm(lam, term)
    return lam


def mobius_mu(n: int) -> int:
    """Mobius function mu(n) for positive integer n."""
    if n == 1:
        return 1
    factors = factorize(n)
    for exp in factors.values():
        if exp > 1:
            return 0
    return -1 if (len(factors) % 2 == 1) else 1
