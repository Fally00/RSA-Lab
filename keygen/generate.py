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

def generate_prime(bits):
    validate_bits(bits)

    while True:
        candidate = secrets.randbits(bits)
        candidate |= (1 << (bits - 1))
        candidate |= 1

        if miller_rabin(candidate)["is_probable_prime"]:
            return candidate

def generate_strong_key(bits=1024):
    validate_bits(bits, minimum=32)

    if bits % 2 != 0:
        raise ValueError("bits must be an even number.")

    e = 65537
    prime_bits = bits // 2
    min_distance = 1 << max(0, prime_bits - 100)

    while True:
        p = generate_prime(prime_bits)
        q = generate_prime(prime_bits)

        if p == q:
            continue

        if abs(p - q) < min_distance:
            continue

        n = p * q

        if n.bit_length() != bits:
            continue

        phi = (p - 1) * (q - 1)

        if gcd(e, phi) != 1:
            continue

        d = modinv(e, phi)
        break

    return {
        "n": n,
        "e": e,
        "d": d,
        "p": p,
        "q": q,
        "bits": bits
    }

def generate_weak_key(bits=1024, kind="small_primes"):
    validate_bits(bits)

    from keygen.weak_keys import generate_demo_weak_key

    return generate_demo_weak_key(bits, kind)