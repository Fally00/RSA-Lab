"Purpose: W9: modinv, modpow (square-and-multiply), crt."

from core.euclid import extended_gcd, gcd


def modinv(a, m, return_steps=False):
    "Find x in [0, m-1] such that (a * x) % m == 1."
    if m <= 0:
        raise ValueError("m must be positive")

    if return_steps:
        (g, x, y), steps = extended_gcd(a, m, return_steps=True)
    else:
        g, x, y = extended_gcd(a, m)
        steps = []

    if g != 1:
        raise ValueError(f"No inverse: gcd({a}, {m}) = {g} != 1")

    inv = x % m
    if return_steps:
        steps.append(f"inverse = {x} % {m} = {inv}")
        return inv, steps
    return inv


def modpow(base, exp, mod, return_steps=False):
    "Compute (base ** exp) % mod using square-and-multiply."
    if mod <= 0:
        raise ValueError("mod must be positive")
    if mod == 1:
        return (0, ["anything mod 1 is 0"]) if return_steps else 0

    steps = []
    if exp < 0:
        base = modinv(base, mod)
        exp = -exp
        if return_steps:
            steps.append(f"negative exp -> inverted base to {base}, exp = {exp}")

    result = 1
    base = base % mod

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
            if return_steps:
                steps.append(f"exp={exp} (odd): result = {result}")
        elif return_steps:
            steps.append(f"exp={exp} (even): result stays {result}")

        base = (base * base) % mod
        exp = exp // 2
        if return_steps and exp > 0:
            steps.append(f"square base -> {base}, next exp = {exp}")

    if return_steps:
        steps.append(f"answer = {result}")
        return result, steps
    return result


def crt(remainders, moduli, return_steps=False):
    """Solve x = r_i (mod m_i) using the Chinese Remainder Theorem. Returns (x, M)."""
    if len(remainders) == 0 or len(remainders) != len(moduli):
        raise ValueError("remainders and moduli must have the same non-zero length")

    for m in moduli:
        if m <= 0:
            raise ValueError("all moduli must be positive")

    # check pairwise coprime
    for i in range(len(moduli)):
        for j in range(i + 1, len(moduli)):
            if gcd(moduli[i], moduli[j]) != 1:
                raise ValueError(f"moduli {moduli[i]} and {moduli[j]} are not coprime")

    M = 1
    for m in moduli:
        M *= m

    steps = []
    if return_steps:
        steps.append(f"M = {M}")

    total = 0
    for i in range(len(moduli)):
        r_i = remainders[i] % moduli[i]
        m_i = moduli[i]
        M_i = M // m_i
        y_i = modinv(M_i, m_i)
        total = (total + r_i * M_i * y_i) % M
        if return_steps:
            steps.append(f"i={i + 1}: M_i={M_i}, y_i={y_i}, term={r_i}*{M_i}*{y_i}")

    if return_steps:
        steps.append(f"x = {total} (mod {M})")
        return (total, M), steps
    return (total, M)
