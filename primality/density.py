"""
primality/density.py
Owner: Member 5(Haneen)
Purpose: W8: tries needed to find a prime vs the 1/ln(n) prediction.
"""

import math
from .miller_rabin import miller_rabin

def prime_density_experiment(n):
    steps = [f"Starting prime density experiment around n = {n}."]

    if not isinstance(n, int) or isinstance(n, bool) or n < 3:
        raise ValueError("n must be an integer greater than or equal to 3.")

    expected_tries = math.log(n) / 2
    steps.append(
        f"Expected odd-number tries around n is approximately ln({n}) / 2 = {expected_tries:.2f}."
    )

    actual_tries = 0
    current = n

    if current % 2 == 0:
        steps.append(f"Skipping even number {current}.")
        current += 1
        steps.append(f"Starting search from odd number {current}.")

    while True:
        actual_tries += 1
        steps.append(f"Try {actual_tries}: testing {current}.")

        result = miller_rabin(current)

        if result["is_probable_prime"]:
            steps.append(
                f"Found a probable prime: {current} after {actual_tries} tries."
            )
            break

        steps.append(f"{current} is composite. Moving to the next odd number.")
        current += 2

    steps.append(f"Actual tries = {actual_tries}.")
    steps.append(f"Expected odd-number tries ≈ {expected_tries:.2f}.")

    return {
        "n": n,
        "found_prime": current,
        "actual_tries": actual_tries,
        "expected_tries": expected_tries,
        "steps": steps
    }


def run_density_averages(start_n, step, count):
    if count < 1:
        raise ValueError("count must be at least 1.")

    results = []
    total_actual = 0
    total_expected = 0.0

    for i in range(count):
        n = start_n + (i * step)
        exp_result = prime_density_experiment(n)
        
        results.append(exp_result)
        total_actual += exp_result["actual_tries"]
        total_expected += exp_result["expected_tries"]

    return {
        "results": results,
        "average_actual": total_actual / count,
        "average_expected": total_expected / count
    }