"Purpose: W2: gcd, lcm, extended_gcd with step trace."

def gcd(a, b, return_steps=False):
    "Compute gcd(a, b) using the Euclidean algorithm."
    steps = []
    a = abs(a)
    b = abs(b)

    while b != 0:
        q = a // b
        r = a % b
        if return_steps:
            steps.append(f"{a} = {q} * {b} + {r}")
        a, b = b, r

    if return_steps:
        steps.append(f"gcd = {a}")
        return a, steps
    return a

def lcm(a, b, return_steps=False):
    "Compute lcm(a, b) = |a * b| // gcd(a, b)."
    if a == 0 or b == 0:
        if return_steps:
            return 0, ["lcm with 0 is 0"]
        return 0

    if return_steps:
        g, steps = gcd(a, b, return_steps=True)
        ans = abs(a * b) // g
        steps.append(f"lcm({a}, {b}) = |{a} * {b}| // {g} = {ans}")
        return ans, steps

    g = gcd(a, b)
    return abs(a * b) // g

def extended_gcd(a, b, return_steps=False):
    "Return (g, x, y) such that a * x + b * y = g = gcd(a, b)."
    steps = []
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
        if return_steps:
            steps.append(f"q = {q}, r = {r}, s = {s}, t = {t}")

    # keep gcd positive
    if old_r < 0:
        old_r = -old_r
        old_s = -old_s
        old_t = -old_t

    result = (old_r, old_s, old_t)
    if return_steps:
        steps.append(f"{a} * ({old_s}) + {b} * ({old_t}) = {old_r}")
        return result, steps
    return result