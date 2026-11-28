"""
core/__init__.py
Owner: Omar Tarek
Purpose: Export all core math functions.
"""

from core.divisibility import divides, division_algorithm, is_even, is_odd, parity
from core.euclid import gcd, extended_gcd, lcm
from core.diophantine import solve_diophantine
from core.modular import modinv, modpow, crt
from core.roots import isqrt, is_perfect_square

__all__ = [
    "divides",
    "division_algorithm",
    "is_even",
    "is_odd",
    "parity",
    "gcd",
    "extended_gcd",
    "lcm",
    "solve_diophantine",
    "modinv",
    "modpow",
    "crt",
    "isqrt",
    "is_perfect_square",
]
