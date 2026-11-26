"""Batch GCD attack for RSA moduli that accidentally share a prime."""

import math
import time

from audit.contract import derive_private_key, make_result
from audit.parser import parse_key
from primality.miller_rabin import miller_rabin


def _modulus(key):
    """Accept the (n, e), {n, e}, or bare-n forms used by the audit layer."""
    if isinstance(key, dict):
        n, e = parse_key(key)
    elif isinstance(key, (list, tuple)) and len(key) == 2:
        n, e = key
    else:
        n, e = key, None
    if type(n) is not int or n <= 1:
        raise ValueError("each key must contain an integer modulus n > 1")
    if e is not None and (type(e) is not int or e <= 1):
        raise ValueError("public exponent e must be an integer greater than 1")
    return n, e


def product_tree(values):
    """Return the levels of a product tree (empty input gives an empty tree)."""
    values = list(values)
    if any(type(value) is not int or value <= 0 for value in values):
        raise ValueError("product tree values must be positive integers")
    if not values:
        return []
    levels = [list(values)]
    while len(levels[-1]) > 1:
        level = levels[-1]
        levels.append([level[i] * level[i + 1] if i + 1 < len(level) else level[i]
                       for i in range(0, len(level), 2)])
    return levels


def batch_gcd(moduli):
    """Return gcd(n_i, product of all other moduli) for each modulus."""
    moduli = list(moduli)
    if any(type(n) is not int or n <= 1 for n in moduli):
        raise ValueError("moduli must be integers greater than 1")
    if len(moduli) < 2:
        return [1] * len(moduli)

    # Remainder-tree descent computes P mod n_i^2 without constructing one
    # separate product for every key. Duplicate moduli naturally yield n_i.
    levels = product_tree(moduli)
    remainders = [levels[-1][0]]
    for level in reversed(levels[:-1]):
        next_remainders = []
        for index, modulus in enumerate(level):
            parent = remainders[index // 2]
            next_remainders.append(parent % (modulus * modulus))
        remainders = next_remainders
    return [math.gcd((remainder // n), n) for n, remainder in zip(moduli, remainders)]


def run_batch(keys):
    """Run batch GCD and return one shared-contract result per input key."""
    keys = list(keys)
    parsed = [_modulus(key) for key in keys]
    moduli = [n for n, _ in parsed]
    batch_start = time.perf_counter()
    gcds = batch_gcd(moduli)
    per_key_ms = ((time.perf_counter() - batch_start) * 1000 / len(parsed)) if parsed else 0.0
    results = []

    for index, ((n, e), common) in enumerate(zip(parsed, gcds)):
        steps = [f"Compared n[{index}] against the product of all other moduli using batch GCD."]
        factors = private_key = None
        broken = 1 < common < n
        if common == n:
            # When one modulus shares different primes with different peers,
            # the product-tree gcd can be n. Pairwise checks can still isolate
            # a proper factor for this uncommon case.
            for other_index, other in enumerate(moduli):
                if other_index == index:
                    continue
                pair_gcd = math.gcd(n, other)
                if 1 < pair_gcd < n:
                    common = pair_gcd
                    broken = True
                    steps.append(f"Pairwise gcd with n[{other_index}] isolated a proper factor.")
                    break
        if broken:
            p, q = common, n // common
            if p * q == n and p > 1 and q > 1:
                factors = [p, q]
                factors_are_probable_primes = (
                    miller_rabin(p)["is_probable_prime"]
                    and miller_rabin(q)["is_probable_prime"]
                )
                private_key = (derive_private_key(e, p, q)
                               if e is not None and factors_are_probable_primes else None)
                steps.append(f"gcd(n, product of other moduli) = {p}, a proper factor of n.")
                steps.append(f"Recovered factors: {p} * {q} = {n}.")
                if e is not None:
                    steps.append("Recovered private exponent." if private_key is not None
                                 else "Factors found, but e has no inverse for this modulus.")
            else:
                broken = False
        elif common == n:
            steps.append("The gcd equals n; duplicate moduli or multiple shared factors prevent isolating a proper factor.")
        else:
            steps.append("No proper shared factor was found.")

        results.append(make_result(
            "shared_prime", 2, broken=broken, factors=factors,
            private_key=private_key, steps=steps,
            time_ms=per_key_ms,
        ))
    return results
