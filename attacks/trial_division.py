"""
attacks/trial_division.py
Owner: Member 3
Purpose: W3: try small divisors up to sqrt(n).
Follows the shared contract: run(n, e) -> dict (see README section 7).
"""
from math import isqrt


def run(n, e, verbose=True):
    """Trial division attack on a (small) RSA modulus, explained step by step.

    1. Try divisors from 2 up to sqrt(n) and record each step.
    2. When a divisor d divides n, we have p and q = n // p.
    3. Compute phi = (p-1)(q-1).
    4. Compute the private exponent d = e^-1 mod phi.
    """

    def say(text=""):
        if verbose:
            print(text)

    say("=" * 55)
    say(" TRIAL DIVISION ATTACK ON RSA")
    say("=" * 55)
    say(f"Public key:  n = {n}")
    say(f"             e = {e}")
    say()

    # ---- Step 1: trial division ----
    limit = isqrt(n)
    say("[Step 1] Try to divide n by every number from 2 up to sqrt(n)")
    say(f"         sqrt(n) is about {limit}, so we try at most {limit - 1} divisors.")
    say("         (If n = p*q, the smaller factor is always <= sqrt(n).)")
    say()

    steps = []
    p = q = None
    for divisor in range(2, limit + 1):
        found = (n % divisor == 0)
        steps.append((divisor, found))              # record each step

        # print every attempt for small searches, otherwise only a few
        if verbose and (limit <= 50 or divisor <= 5 or divisor % 100 == 0 or found):
            result = "divides n  <-- FOUND!" if found else "no"
            print(f"         try {divisor:>8}: n % {divisor} = {n % divisor:<8} {result}")
        if found:
            p, q = divisor, n // divisor
            break

    if p is None:
        say()
        say("[-] No divisor found: n is prime, or it is not a product of two primes.")
        return None

    say()
    say(f"[Step 2] Factors found after {len(steps)} attempts")
    say(f"         p = {p}")
    say(f"         q = n / p = {n} / {p} = {q}")
    say(f"         check: {p} * {q} = {p * q}")
    say()

    # ---- Step 3: phi ----
    phi = (p - 1) * (q - 1)
    say("[Step 3] Compute Euler's totient")
    say("         phi = (p - 1) * (q - 1)")
    say(f"         phi = ({p} - 1) * ({q} - 1) = {phi}")
    say()

    # ---- Step 4: private exponent ----
    d = pow(e, -1, phi)                             # modular inverse (Python 3.8+)
    say("[Step 4] Compute the private exponent (modular inverse of e)")
    say("         d = e^-1 mod phi")
    say(f"         d = {e}^-1 mod {phi} = {d}")
    say(f"         check: (d * e) mod phi = {(d * e) % phi}  (must be 1)")
    say()

    say("[Done]   Private key recovered!")
    say(f"         Decrypt any ciphertext c with:  m = pow(c, {d}, {n})")
    say("=" * 55)

    return {"p": p, "q": q, "phi": phi, "d": d, "steps": steps}


if __name__ == "__main__":
    print("Trial Division Attack - enter the RSA public key\n")
    try:
        n = int(input("Enter n (modulus): ").strip())
        e = int(input("Enter e (public exponent): ").strip())
    except ValueError:
        print("[-] n and e must be whole numbers.")
        raise SystemExit(1)

    print()
    run(n, e)
