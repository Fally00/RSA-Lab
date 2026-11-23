"""
primality/fermat_test.py
Owner: Member 5(Haneen)
Purpose: W11: Fermat primality test.
"""
from math import gcd
DEFAULT_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)

def fermat_test(n, bases=None):
    steps = [f"Starting Fermat test for n = {n}."]

    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("n must be an integer.")

    if n < 2:
        steps.append("Numbers less than 2 are not prime.")
        return {
            "n": n,
            "is_probable_prime": False,
            "result": "composite",
            "factor": None,
            "witness": None,
            "bases": [],
            "steps": steps
        }

    if n in (2, 3, 5, 7):
        steps.append(f"{n} is a small prime.")
        return {
            "n": n,
            "is_probable_prime": True,
            "result": "prime",
            "factor": None,
            "witness": None,
            "bases": [],
            "steps": steps
        }

    if n % 2 == 0:
        steps.append("The number is even and greater than 2.")
        return {
            "n": n,
            "is_probable_prime": False,
            "result": "composite",
            "factor": 2,
            "witness": None,
            "bases": [],
            "steps": steps
        }

    for p in (3, 5, 7):
        if n % p == 0:
            steps.append(f"{n} is divisible by {p}.")
            return {
                "n": n,
                "is_probable_prime": False,
                "result": "composite",
                "factor": p,
                "witness": None,
                "bases": [],
                "steps": steps
            }

    if bases is None:
        bases = [a for a in DEFAULT_BASES if 2 <= a < n]
        if not bases:
            bases = [2]
        steps.append(f"Using default bases: {bases}.")
    else:
        if not isinstance(bases, (list, tuple)) or not bases:
            raise ValueError("bases must be a non-empty list or tuple.")
        for base in bases:
            if not isinstance(base, int) or isinstance(base, bool):
                raise ValueError("All bases must be integers.")
            if base < 2 or base >= n:
                raise ValueError(f"Base {base} must be between 2 and n-1.")

    tested_bases = []

    for a in bases:
        steps.append(f"Testing base a = {a}.")
        common = gcd(a, n)
        steps.append(f"gcd({a}, {n}) = {common}.")

        if common > 1:
            steps.append(f"Found a non-trivial factor: {common}.")
            return {
                "n": n,
                "is_probable_prime": False,
                "result": "composite",
                "factor": common,
                "witness": None,
                "bases": tested_bases + [a],
                "steps": steps
            }

        tested_bases.append(a)
        remainder = pow(a, n - 1, n)
        steps.append(f"{a}^{n-1} mod {n} = {remainder}.")

        if remainder != 1:
            steps.append("Fermat condition failed. The number is definitely composite.")
            return {
                "n": n,
                "is_probable_prime": False,
                "result": "composite",
                "factor": None,
                "witness": a,
                "bases": tested_bases,
                "steps": steps
            }

        steps.append(f"Base {a} passed Fermat test.")

    steps.append("All tested bases passed. The number is probably prime, not proven prime.")
    return {
        "n": n,
        "is_probable_prime": True,
        "result": "probably_prime",
        "factor": None,
        "witness": None,
        "bases": tested_bases,
        "steps": steps
    }