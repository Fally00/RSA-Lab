"""
attacks/fermat.py
Owner: Member 3
Purpose: W12: Fermat factorization (works when p and q are close).
Follows the shared contract: run(n, e) -> dict (see README section 7).
"""
"""
Fermat's factorization attack on RSA  (attacks/fermat.py)

Idea:
    If n = p * q and p and q are CLOSE to each other, we can write
        n = a^2 - b^2 = (a - b)(a + b)      ->   p = a - b,  q = a + b
    So we search a starting from ceil(sqrt(n)) until  a^2 - n  is a perfect square.
"""

from math import isqrt


def is_perfect_square(x):
    """Return (True, root) if x is a perfect square, else (False, None)."""
    r = isqrt(x)
    return (r * r == x), r


def run(n, e, c=None, max_steps=10_000_000):
    """
    Fermat attack.
    n : RSA modulus
    e : RSA public exponent
    c : (optional) ciphertext to decrypt
    """
    print("\n=== STEP 1: Check the input ===")
    if n % 2 == 0:
        print("n is even -> 2 is a factor. Fermat is not needed.")
        p, q = 2, n // 2
    else:
        print("n is odd -> Fermat's method can be used.")

        print("\n=== STEP 2: Start searching ===")
        a = isqrt(n)
        if a * a < n:
            a += 1                      # a = ceil(sqrt(n))
        print(f"Starting value: a = ceil(sqrt(n)) = {a}")
        print("For each a we test if  a^2 - n  is a perfect square.")

        steps = 0
        while steps < max_steps:
            b2 = a * a - n
            ok, b = is_perfect_square(b2)
            if ok:
                break
            a += 1
            steps += 1
            if steps % 100000 == 0:
                print(f"  ... still searching (tried {steps} values of a)")
        else:
            print("\n[-] Attack failed: p and q are probably not close enough.")
            return None

        print(f"\n[+] Found after {steps + 1} tries!")
        print(f"    a = {a}")
        print(f"    b = {b}   (because a^2 - n = {b2} = b^2)")

        print("\n=== STEP 3: Get the factors ===")
        p, q = a - b, a + b
        print(f"    p = a - b = {p}")
        print(f"    q = a + b = {q}")

    print("\n=== STEP 4: Verify ===")
    if p * q != n:
        print("[-] p * q != n  -> something went wrong.")
        return None
    print("[+] p * q == n  -> factorization is correct.")

    print("\n=== STEP 5: Compute phi and the private key d ===")
    phi = (p - 1) * (q - 1)
    print(f"    phi = (p-1)(q-1) = {phi}")
    try:
        d = pow(e, -1, phi)             # modular inverse of e mod phi
    except ValueError:
        print("[-] e is not invertible mod phi (gcd(e, phi) != 1).")
        return (p, q, None)
    print(f"    d = e^-1 mod phi = {d}")

    if c is not None:
        print("\n=== STEP 6: Decrypt the ciphertext ===")
        m = pow(c, d, n)
        print(f"    m = c^d mod n = {m}")
        try:
            text = m.to_bytes((m.bit_length() + 7) // 8, "big").decode()
            print(f"    As text: {text}")
        except Exception:
            print("    (m is not readable text, use the number above)")

    return p, q, d


def ask_int(message, optional=False):
    """Ask the user for an integer until a valid one is entered."""
    while True:
        value = input(message).strip()
        if optional and value == "":
            return None
        try:
            return int(value)
        except ValueError:
            print("  Please enter a valid whole number.")


if __name__ == "__main__":
    print("=" * 50)
    print("        Fermat Factorization Attack on RSA")
    print("=" * 50)
    print("This works when the two primes p and q are close together.")
    print("Enter your values as decimal numbers.\n")

    n = ask_int("Enter n (modulus): ")
    e = ask_int("Enter e (public exponent, usually 65537): ")
    c = ask_int("Enter c (ciphertext) or press Enter to skip: ", optional=True)

    result = run(n, e, c)

    print("\n" + "=" * 50)
    if result:
        p, q, d = result
        print("RESULT")
        print(f"p = {p}")
        print(f"q = {q}")
        print(f"d = {d}")
    else:
        print("No result.")
