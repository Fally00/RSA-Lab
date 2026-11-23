"Purpose: W4: solvability test and general solution of ax + by = c."

from core.euclid import extended_gcd


def solve_diophantine(a, b, c, return_steps=False):
    "Solve a*x + b*y = c for integer solutions."
    if a == 0 and b == 0:
        raise ValueError("a and b cannot both be 0")

    if return_steps:
        (d, u, v), steps = extended_gcd(a, b, return_steps=True)
    else:
        d, u, v = extended_gcd(a, b)
        steps = []

    if c % d != 0:
        result = {
            "solvable": False,
            "gcd": d,
            "x0": None,
            "y0": None,
            "x_step": None,
            "y_step": None,
            "general_x": None,
            "general_y": None,
        }
        if return_steps:
            steps.append(f"gcd({a}, {b}) = {d} does not divide {c} -> no solution")
            return result, steps
        return result

    scale = c // d
    x0 = u * scale
    y0 = v * scale
    x_step = b // d
    y_step = -(a // d)

    general_x = f"{x0} + ({x_step})t"
    general_y = f"{y0} + ({y_step})t"

    result = {
        "solvable": True,
        "gcd": d,
        "x0": x0,
        "y0": y0,
        "x_step": x_step,
        "y_step": y_step,
        "general_x": general_x,
        "general_y": general_y,
    }

    if return_steps:
        steps.append(f"{d} divides {c} (scale = {scale})")
        steps.append(f"particular solution: x0 = {x0}, y0 = {y0}")
        steps.append(f"general solution: x = {general_x}, y = {general_y}")
        return result, steps
    return result
