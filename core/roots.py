"Purpose: Integer square root and perfect-square test (used by Fermat)."

def isqrt(n, return_steps=False):
    "Compute floor(sqrt(n)) using integer Newton's method."
    if n < 0:
        raise ValueError("n must be non-negative")

    steps = []
    x = n
    y = (x + 1) // 2

    while y < x:
        if return_steps:
            steps.append(f"x = {x} -> next = {y}")
        x = y
        y = (x + n // x) // 2

    if return_steps:
        steps.append(f"isqrt({n}) = {x}")
        return x, steps
    return x


def is_perfect_square(n, return_steps=False):
    "Return True if n is a perfect square, False otherwise."
    if n < 0:
        if return_steps:
            return False, [f"{n} is negative -> not a square"]
        return False

    if return_steps:
        s, steps = isqrt(n, return_steps=True)
        ans = (s * s == n)
        steps.append(f"{s}^2 = {s * s} {'==' if ans else '!='} {n} -> {ans}")
        return ans, steps

    s = isqrt(n)
    return s * s == n
