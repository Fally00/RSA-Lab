"""Recover and predict a linear congruential generator from observed outputs."""

import math


def _combine_congruences(a, modulus_a, b, modulus_b):
    """Combine x=a (mod modulus_a), x=b (mod modulus_b), if consistent."""
    common = math.gcd(modulus_a, modulus_b)
    difference = b - a
    if difference % common:
        raise ValueError("outputs are inconsistent with an LCG")
    right_modulus = modulus_b // common
    if right_modulus == 1:
        multiplier = 0
    else:
        multiplier = (difference // common) * pow(modulus_a // common, -1, right_modulus)
        multiplier %= right_modulus
    combined_modulus = modulus_a * right_modulus
    return (a + modulus_a * multiplier) % combined_modulus, combined_modulus


def recover_lcg(outputs, m):
    """Return ``(a, c)`` for x[n+1] = (a*x[n] + c) mod m.

    At least three observations are required. Non-invertible differences are
    handled as congruences; an underdetermined multiplier is reported clearly.
    """
    if type(m) is not int or m <= 1:
        raise ValueError("modulus m must be an integer greater than 1")
    if not isinstance(outputs, (list, tuple)) or len(outputs) < 3:
        raise ValueError("at least three outputs are required")
    if any(type(x) is not int or not 0 <= x < m for x in outputs):
        raise ValueError("each output must be an integer in the range 0 <= x < m")

    residue, modulus = 0, 1
    for i in range(len(outputs) - 2):
        difference = outputs[i + 1] - outputs[i]
        target = outputs[i + 2] - outputs[i + 1]
        divisor = math.gcd(difference, m)
        if target % divisor:
            raise ValueError("outputs are inconsistent with an LCG")
        reduced_modulus = m // divisor
        if reduced_modulus == 1:
            continue
        coefficient = (difference // divisor) % reduced_modulus
        target = (target // divisor) % reduced_modulus
        candidate = target * pow(coefficient, -1, reduced_modulus) % reduced_modulus
        residue, modulus = _combine_congruences(
            residue, modulus, candidate, reduced_modulus
        )

    if modulus != m:
        raise ValueError("outputs do not uniquely determine the LCG multiplier")
    a = residue
    c = (outputs[1] - a * outputs[0]) % m
    if any((a * x + c) % m != y for x, y in zip(outputs, outputs[1:])):
        raise ValueError("outputs are inconsistent with an LCG")
    return a, c


def predict_next(last, a, c, m):
    """Predict one output after ``last`` using recovered LCG parameters."""
    if any(type(value) is not int for value in (last, a, c, m)) or m <= 1:
        raise ValueError("last, a, c must be integers and m must be greater than 1")
    return (a * last + c) % m


def predict(outputs, a, c, m, count=1):
    """Return ``count`` future outputs, beginning after the final observation."""
    if not isinstance(outputs, (list, tuple)) or not outputs:
        raise ValueError("at least one observed output is required")
    if type(count) is not int or count < 0:
        raise ValueError("count must be a non-negative integer")
    values = []
    current = outputs[-1]
    for _ in range(count):
        current = predict_next(current, a, c, m)
        values.append(current)
    return values


def main():
    try:
        m = int(input("Enter modulus m: "))
        outputs = [int(value) for value in input(
            "Enter at least 3 outputs (separated by spaces): "
        ).split()]
        a, c = recover_lcg(outputs, m)
        count = int(input("How many next values to predict? "))
        if count < 0:
            raise ValueError("prediction count must be non-negative")
    except (ValueError, EOFError) as exc:
        print(f"Error: {exc}")
        return
    print(f"Recovered: a = {a}, c = {c}")
    for index, value in enumerate(predict(outputs, a, c, m, count), start=1):
        print(f"Next {index}: {value}")


if __name__ == "__main__":
    main()
