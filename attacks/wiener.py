"""
attacks/wiener.py
Owner: Member 4
Purpose: W5: small-d attack using continued fractions; put the convergents table in steps.
Follows the shared contract: run(n, e) -> dict (see README section 7).
"""
"""
Wiener's Attack on RSA
-----------------------
Recovers the private exponent d (and factors p, q) when e/n has a
continued-fraction convergent close enough to d's hidden relation:

    e*d = 1 + k*phi(n)   =>   e/n ~ k/d

Steps performed by run(n, e):
  1. Expand e/n as a continued fraction.
  2. Generate each convergent k/d from that expansion.
  3. For each convergent, compute candidate phi(n) = (e*d - 1) / k.
  4. Solve x^2 - (n - phi(n) + 1)x + n = 0 for p, q and check they are
     valid integer factors of n.

Usage:
    python wiener.py
    (then type n and e when prompted)
"""

from math import isqrt


def continued_fraction(num, den):
    """Step 1: expand num/den as a continued fraction -> list of terms."""
    cf = []
    while den:
        q = num // den
        cf.append(q)
        num, den = den, num - q * den
    return cf


def convergents(cf):
    """Step 2: turn continued fraction terms into convergents k/d."""
    convs = []
    for i in range(len(cf)):
        num, den = cf[i], 1
        for j in range(i - 1, -1, -1):
            num, den = cf[j] * num + den, num
        convs.append((num, den))  # (k, d)
    return convs


def is_perfect_square(x):
    if x < 0:
        return False, 0
    r = isqrt(x)
    return r * r == x, r


def try_candidate(n, e, k, d):
    """Steps 3-4: build phi(n), solve the quadratic, check p,q are factors."""
    if k == 0:
        return None

    # Step 3: candidate phi(n) = (e*d - 1) / k
    if (e * d - 1) % k != 0:
        return None
    phi = (e * d - 1) // k
    if phi <= 0:
        return None

    # Step 4: p, q are roots of x^2 - (n - phi + 1)x + n = 0
    b = n - phi + 1
    discriminant = b * b - 4 * n
    is_sq, sqrt_disc = is_perfect_square(discriminant)
    if not is_sq:
        return None

    if (b - sqrt_disc) % 2 != 0:
        return None

    p = (b - sqrt_disc) // 2
    q = (b + sqrt_disc) // 2

    if p * q == n and p > 1 and q > 1:
        return p, q, d
    return None


def run(n, e):
    """
    Full Wiener attack pipeline:
      expand e/n -> test each convergent k/d -> compute phi candidate ->
      solve quadratic for p, q.
    Prints the convergents table and the result.
    """
    print(f"\n[*] Target modulus n = {n}")
    print(f"[*] Public exponent e = {e}\n")

    print("[Step 1] Expanding e/n as a continued fraction...")
    cf = continued_fraction(e, n)
    print(f"    Continued fraction terms: {cf}\n")

    print("[Step 2] Generating convergents k/d...")
    convs = convergents(cf)

    print("\n{:<6} {:<25} {:<25}".format("i", "k", "d"))
    print("-" * 60)
    for i, (k, d) in enumerate(convs):
        print("{:<6} {:<25} {:<25}".format(i, k, d))
    print()

    print("[Step 3 & 4] Testing each convergent as a candidate (k, d)...")
    for i, (k, d) in enumerate(convs):
        result = try_candidate(n, e, k, d)
        if result:
            p, q, d_found = result
            print(f"\n[+] SUCCESS at convergent #{i}: k={k}, d={d}")
            print(f"[+] Private exponent d = {d_found}")
            print(f"[+] p = {p}")
            print(f"[+] q = {q}")
            return {"d": d_found, "p": p, "q": q}

    print("\n[-] Attack failed: d is not small enough relative to n,")
    print("    or e/n's convergents did not reveal it (n may be 'safe').")
    return None


if __name__ == "__main__":
    print("=== Wiener's Attack on RSA ===")
    print("This recovers a small private key d from a public key (n, e).\n")
    print("Steps the program will follow:")
    print("  1. Expand e/n into a continued fraction")
    print("  2. Build the convergents k/d from that expansion")
    print("  3. For each convergent, compute a candidate phi(n)")
    print("  4. Solve the quadratic x^2 - (n - phi + 1)x + n = 0 for p, q")
    print("  5. Check if p*q == n -> if so, d is the private key\n")

    try:
        n = int(input("Enter n (modulus): ").strip())
        e = int(input("Enter e (public exponent): ").strip())
    except ValueError:
        print("Invalid input: n and e must be integers.")
        raise SystemExit(1)

    run(n, e)
