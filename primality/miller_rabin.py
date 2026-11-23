"""
primality/miller_rabin.py
Owner: Member 5(Haneen)
Purpose: W11: Miller-Rabin with a witness trace in steps.
"""
DEFAULT_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)

def miller_rabin(n, bases=None):
    steps = [f"Starting Miller-Rabin test for n = {n}."]

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
        bases = [a for a in DEFAULT_BASES if 2 <= a <= n - 2]
        if not bases:
            bases = [2]
        steps.append(f"Using default bases: {bases}.")
    else:
        if not isinstance(bases, (list, tuple)) or not bases:
            raise ValueError("bases must be a non-empty list or tuple.")
        for base in bases:
            if not isinstance(base, int) or isinstance(base, bool):
                raise ValueError("All bases must be integers.")
            if base < 2 or base > n - 2:
                raise ValueError(f"Base {base} must be between 2 and n-2.")

    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    steps.append(f"n - 1 = {n - 1} = 2^{s} * {d}.")

    tested_bases = []

    for a in bases:
        steps.append(f"Testing base a = {a}.")

        x = pow(a, d, n)
        tested_bases.append(a)
        steps.append(f"x0 = {a}^{d} mod {n} = {x}.")

        if x == 1 or x == n - 1:
            steps.append(f"x0 is 1 or n-1, so base {a} is not a witness.")
            continue

        is_witness = True

        for i in range(1, s):
            x = pow(x, 2, n)
            steps.append(f"x{i} = x{i-1}^2 mod {n} = {x}.")

            if x == n - 1:
                steps.append(f"x{i} = n-1, so base {a} is not a witness.")
                is_witness = False
                break

            if x == 1:
                steps.append(f"x{i} = 1 before reaching n-1.")
                break

        if is_witness:
            steps.append(f"Base {a} is a WITNESS. The number is definitely composite.")
            return {
                "n": n,
                "is_probable_prime": False,
                "result": "composite",
                "factor": None,
                "witness": a,
                "bases": tested_bases,
                "steps": steps
            }

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