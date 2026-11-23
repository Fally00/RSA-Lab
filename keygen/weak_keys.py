from math import gcd, isqrt

from keygen.generate import generate_prime, validate_bits
from core.modular import modinv
from primality import miller_rabin


def _pack_key(p, q, e=65537, bits=None, d=None):
    phi = (p - 1) * (q - 1)
    n = p * q

    if d is not None:
        e = modinv(d, phi)
    else:
        if gcd(e, phi) != 1:
            e = 3
            while e < phi and gcd(e, phi) != 1:
                e += 2

        if e >= phi:
            raise ValueError("Could not find a valid public exponent.")

        d = modinv(e, phi)

    return {
        "n": n,
        "e": e,
        "d": d,
        "p": p,
        "q": q,
        "bits": bits if bits is not None else n.bit_length(),
        "actual_bits": n.bit_length()
    }


def _small_primes(bits):
    p = generate_prime(16)
    q = generate_prime(16)

    while p == q:
        q = generate_prime(16)

    return _pack_key(p, q, bits=bits)


def _next_prime_after(n):
    candidate = n + 1

    if candidate % 2 == 0:
        candidate += 1

    while not miller_rabin(candidate)["is_probable_prime"]:
        candidate += 2

    return candidate


def _close_primes(bits):
    prime_bits = bits // 2

    while True:
        p = generate_prime(prime_bits)
        q = _next_prime_after(p)

        while q.bit_length() == prime_bits and q - p >= 1000:
            p = q
            q = _next_prime_after(q)

        if q.bit_length() != prime_bits:
            continue

        if (p * q).bit_length() != bits:
            continue

        return _pack_key(p, q, bits=bits)


def _small_d(bits):
    prime_bits = bits // 2

    while True:
        p = generate_prime(prime_bits)
        q = generate_prime(prime_bits)

        if p == q:
            continue

        n = p * q

        if n.bit_length() != bits:
            continue

        phi = (p - 1) * (q - 1)
        fourth_root = isqrt(isqrt(n))
        max_d = (fourth_root - 1) // 3

        d = 3

        while d <= max_d:
            if gcd(d, phi) == 1:
                return _pack_key(p, q, bits=bits, d=d)

            d += 2


def _shared_prime(bits):
    prime_bits = bits // 2
    p_shared = generate_prime(prime_bits)

    while True:
        p1 = generate_prime(prime_bits)

        if p1 == p_shared:
            continue

        if (p_shared * p1).bit_length() == bits:
            break

    while True:
        p2 = generate_prime(prime_bits)

        if p2 == p_shared or p2 == p1:
            continue

        if (p_shared * p2).bit_length() == bits:
            break

    key1 = _pack_key(p_shared, p1, bits=bits)
    key2 = _pack_key(p_shared, p2, bits=bits)

    return key1, key2


def generate_demo_weak_key(bits=1024, kind="small_primes"):
    validate_bits(bits, minimum=32)

    if bits % 2 != 0:
        raise ValueError("bits must be an even number.")

    if kind == "small_primes":
        return _small_primes(bits)

    elif kind == "close_primes":
        return _close_primes(bits)

    elif kind == "small_d":
        if bits < 64:
            raise ValueError("small_d requires at least 64 bits.")
        return _small_d(bits)

    elif kind == "shared_prime":
        return _shared_prime(bits)

    else:
        raise ValueError(f"Unknown weak key kind: {kind}")
    