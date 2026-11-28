"""
keygen/generate.py
Owner: Member 5(Haneen)
Purpose: generate_prime(bits) and generate_strong_key(bits).
"""

import secrets
from math import gcd

from primality import miller_rabin
from core.modular import modinv

def validate_bits(bits, minimum=16):
    if not isinstance(bits, int) or isinstance(bits, bool):
        raise ValueError("bits must be an integer.")

    if bits < minimum:
        raise ValueError(f"bits must be at least {minimum}.")

def generate_prime(bits, minimum=16):
    validate_bits(bits, minimum=minimum)

    while True:
        candidate = secrets.randbits(bits)
        candidate |= (1 << (bits - 1))
        candidate |= 1

        if miller_rabin(candidate)["is_probable_prime"]:
            return candidate

def generate_strong_key(bits=1024, e=None, seed=None):
    validate_bits(bits, minimum=12)

    if bits % 2 != 0:
        raise ValueError("bits must be an even number.")

    prime_bits = bits // 2
    min_distance = 1 << max(0, prime_bits - 100)

    if e is None:
        e = 17 if bits <= 16 else 65537
    if isinstance(e, bool) or not isinstance(e, int) or e <= 1:
        raise ValueError("e must be an integer greater than 1.")

    if seed is not None:
        if not isinstance(seed, (tuple, list)) or len(seed) != 2:
            raise ValueError("seed must contain two prime values (p, q).")
        p, q = seed
        if any(isinstance(value, bool) or not isinstance(value, int) for value in (p, q)):
            raise ValueError("seed values p and q must be integers.")
        if p == q or not all(miller_rabin(value)["is_probable_prime"] for value in (p, q)):
            raise ValueError("seed values must be distinct primes.")
        if (p * q).bit_length() != bits:
            raise ValueError(f"seed primes must produce a {bits}-bit modulus.")
        phi = (p - 1) * (q - 1)
        if e >= phi or gcd(e, phi) != 1:
            raise ValueError("e must be less than phi(n) and coprime to it.")
        d = modinv(e, phi)
        return _key_result(p, q, bits, e, d, phi)

    while True:
        p = generate_prime(prime_bits, minimum=max(2, min(16, prime_bits)))
        q = generate_prime(prime_bits, minimum=max(2, min(16, prime_bits)))

        if p == q:
            continue

        if abs(p - q) < min_distance:
            continue

        n = p * q

        if n.bit_length() != bits:
            continue

        phi = (p - 1) * (q - 1)

        if e >= phi or gcd(e, phi) != 1:
            continue

        d = modinv(e, phi)
        break

    return _key_result(p, q, bits, e, d, phi)


def _key_result(p, q, bits, e, d, phi):
    n = p * q
    return {
        "n": n,
        "e": e,
        "d": d,
        "p": p,
        "q": q,
        "bits": bits,
        "phi": phi,
        "steps": [
            f"Choose distinct primes p = {p} and q = {q}.",
            f"Compute n = p × q = {n}.",
            f"Compute phi(n) = (p - 1)(q - 1) = {phi}.",
            f"Check gcd(e, phi(n)) = gcd({e}, {phi}) = 1.",
            f"Compute d = e⁻¹ mod phi(n) = {d}.",
        ],
    }

def generate_weak_key(bits=1024, kind="small_primes"):
    validate_bits(bits)

    from keygen.weak_keys import generate_demo_weak_key

    return generate_demo_weak_key(bits, kind)
