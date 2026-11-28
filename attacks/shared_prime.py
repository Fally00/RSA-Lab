"""
attacks/shared_prime.py
Owner: Member 6
Purpose: W2: batch gcd across many keys to find shared primes.
Follows the shared contract: run_batch(keys) -> list[dict] (see README section 7).
"""
import math
import time
from audit.contract import make_result, elapsed_time, derive_private_key, table


def find_gcd(A, B):
    if A > B:
        result = math.gcd(A, B)
        print("GCD = ", result)
    elif B > A:
        A, B = B, A
        result = math.gcd(A, B)
        print("GCD = ", result)
    else:
        print("Please inter valid numbers")


# =================BATCH GCD=============================#

def product_tree(x: list[int]) -> list[list[int]]:
    tree = [x]
    while len(x) > 1:
        x = [math.prod(x[i * 2:(i + 1) * 2]) for i in range((len(x) + 1) // 2)]  # if x odd
        tree.append(x)
    return tree


def batch_gcd(x: list[int]) -> list[int]:
    if not x:
        return []
    elif len(x) == 1:
        return [1]
    prod = product_tree(x)
    remove = prod.pop()
    while prod:
        level = prod.pop()
        remove = [remove[i // 2] % (level[i] ** 2) for i in range(len(level))]
    return [math.gcd(r // n, n) for r, n in zip(remove, x)]


def run_batch(keys):
    """Run batch GCD across a list of keys (dicts with n/e/label or (n, e) tuples)."""
    parsed = []
    for idx, k in enumerate(keys):
        if isinstance(k, dict):
            parsed.append((int(k["n"]), int(k["e"]), k.get("label", f"key-{idx + 1}")))
        else:
            parsed.append((int(k[0]), int(k[1]), f"key-{idx + 1}"))

    results = []
    for i, (n_i, e_i, label_i) in enumerate(parsed):
        start = time.perf_counter()
        rows = []
        shared_p = None
        for j, (n_j, _, label_j) in enumerate(parsed):
            if i == j:
                continue
            g = math.gcd(n_i, n_j)
            rows.append([f"{label_i} x {label_j}", str(g)])
            if 1 < g < n_i and shared_p is None:
                shared_p = g

        steps = [
            "Compute gcd(n_i, n_j) for every pair (W2 Euclid). A gcd strictly between 1 and n is a shared prime, which factors both keys instantly.",
            table(["pair", "gcd"], rows),
        ]

        if shared_p is not None:
            q = n_i // shared_p
            d = derive_private_key(e_i, shared_p, q)
            steps.append(f"Shared prime {shared_p} found. n = {q} x {shared_p}")
            results.append(
                make_result(
                    "shared_prime",
                    2,
                    broken=True,
                    factors=sorted([shared_p, q]),
                    private_key=d,
                    steps=steps,
                    time_ms=elapsed_time(start),
                )
            )
        else:
            steps.append("All gcds are 1: this key shares no prime with the others in the batch.")
            results.append(
                make_result(
                    "shared_prime",
                    2,
                    broken=False,
                    steps=steps,
                    time_ms=elapsed_time(start),
                )
            )

    return results


if __name__ == "__main__":
    A = int(input("Enter your greatest num = "))
    B = int(input("Enter your secound  num = "))
    find_gcd(A, B)

    num = int(input("Enter how many numbers of key  = "))
    key = []
    for i in range(num):
        n = int(input(f"Enter RSA key {i+1} = "))
        key.append(n)
    print(batch_gcd(key))