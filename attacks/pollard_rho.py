"""
attacks/pollard_rho.py
Owner: Member 3
Purpose: W12: Pollard's rho factoring.
Follows the shared contract: run(n, e) -> dict (see README section 7).
"""
"""
Pollard's Rho attack on RSA (Floyd cycle detection)
f(x) = x^2 + c mod n
Works when n = p * q and one of the primes is relatively small.
"""

from math import gcd


def f(x, c, n):
    """The pseudo-random function: f(x) = x^2 + c mod n"""
    return (x * x + c) % n


MAX_ITERATIONS = 1_000_000
MAX_C_RETRIES  = 20


def run(n, e):
    """Factor n with Pollard's rho, then recover the private key d."""
    print("\n[Step 1] Looking for a factor of n using Floyd cycle detection...")

    if n % 2 == 0:
        p = 2
    else:
        p = None
        c = 1
        while p is None and c <= MAX_C_RETRIES:
            x, y, d = 2, 2, 1           # tortoise (x) and hare (y)
            iters = 0
            while d == 1 and iters < MAX_ITERATIONS:
                x = f(x, c, n)          # tortoise moves 1 step
                y = f(f(y, c, n), c, n) # hare moves 2 steps
                d = gcd(abs(x - y), n)  # check for a common factor
                iters += 1
            if d not in (1, n):
                p = d                   # found a real factor
            else:
                print(f"    c = {c} failed (cycle found, no factor). Trying c = {c + 1}")
                c += 1

        if p is None:
            print("[-] Attack failed: no factor found within iteration limits.")
            return None

    q = n // p
    print(f"[Step 2] Factors found: p = {p}, q = {q}")
    print(f"         Check: p * q = {p * q} -> {'OK' if p * q == n else 'WRONG'}")

    phi = (p - 1) * (q - 1)
    print(f"[Step 3] Euler's totient: phi(n) = (p-1)*(q-1) = {phi}")

    d = pow(e, -1, phi)
    print(f"[Step 4] Private key: d = e^-1 mod phi(n) = {d}")

    return p, q, d


def main():
    print("=== Pollard's Rho Attack on RSA ===")
    print("You will enter the PUBLIC key (n, e). The attack will find the private key.\n")

    try:
        n = int(input("Step 1 - Enter the modulus n (positive integer): "))
        e = int(input("Step 2 - Enter the public exponent e (e.g. 65537): "))
    except ValueError:
        print("Error: please enter whole numbers only.")
        return

    if n < 4 or e < 2:
        print("Error: n must be >= 4 and e must be >= 2.")
        return

    try:
        p, q, d = run(n, e)
    except ValueError:
        print("Error: e has no inverse mod phi(n) (gcd(e, phi) != 1). Check your inputs.")
        return

    print("\n=== Result ===")
    print(f"p = {p}\nq = {q}\nd = {d}")

    choice = input("\nDo you want to decrypt a ciphertext? (y/n): ").strip().lower()
    if choice == "y":
        try:
            ct = int(input("Enter the ciphertext (integer): "))
        except ValueError:
            print("Error: ciphertext must be an integer.")
            return
        m = pow(ct, d, n)
        print(f"Decrypted number: {m}")
        try:
            text = m.to_bytes((m.bit_length() + 7) // 8, "big").decode()
            print(f"As text: {text}")
        except Exception:
            print("(Could not convert to text, the number above is the plaintext.)")


if __name__ == "__main__":
    main()
