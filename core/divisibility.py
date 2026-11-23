"Purpose: W1: divides check, division algorithm (quotient/remainder), parity helpers."


def divides(a, b, return_steps=False):
    "Return True if a divides b (a | b)."
    steps = []

    if a == 0:
        ans = (b == 0)
        steps.append(f"0 divides {b}: {ans}")
    else:
        r = b % a
        ans = (r == 0)
        if ans:
            steps.append(f"{b} = {b // a} * {a}, so {a} | {b}")
        else:
            steps.append(f"{b} % {a} = {r} != 0, so {a} does not divide {b}")

    if return_steps:
        return ans, steps
    return ans


def division_algorithm(a, d, return_steps=False):
    "Return (q, r) such that a = d * q + r and 0 <= r < d."
    if d <= 0:
        raise ValueError("d must be positive")

    q = a // d
    r = a - d * q
    steps = [
        f"q = {a} // {d} = {q}",
        f"r = {a} - {d} * {q} = {r}",
        f"{a} = {d} * ({q}) + {r}",
    ]

    if return_steps:
        return (q, r), steps
    return (q, r)


def is_even(n, return_steps=False):
    "Return True if n is even."
    ans = (n % 2 == 0)
    steps = [f"{n} % 2 = {n % 2} -> even: {ans}"]
    if return_steps:
        return ans, steps
    return ans


def is_odd(n, return_steps=False):
    "Return True if n is odd."
    ans = (n % 2 != 0)
    steps = [f"{n} % 2 = {n % 2} -> odd: {ans}"]
    if return_steps:
        return ans, steps
    return ans


def parity(n, return_steps=False):
    "Return 'even' or 'odd'."
    r = n % 2
    ans = "even" if r == 0 else "odd"
    steps = [f"{n} = 2 * ({n // 2}) + {r} -> {ans}"]
    if return_steps:
        return ans, steps
    return ans
