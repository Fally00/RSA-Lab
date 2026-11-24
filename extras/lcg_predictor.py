"""
extras/lcg_predictor.py
Owner: Member 6
Purpose: STRETCH (W13): predict an LCG random generator from its outputs. Standalone, not wired into the audit.
"""
def recover_lcg(outputs, m):
    x1, x2, x3 = outputs[0], outputs[1], outputs[2]
    a = ((x3 - x2) * pow(x2 - x1, -1, m)) % m
    c = (x2 - a * x1) % m
    return a, c


def predict_next(last, a, c, m):
    return (a * last + c) % m


def main():
    m = int(input("Enter modulus m: "))

    raw = input("Enter at least 3 outputs (separated by spaces): ")
    outputs = [int(x) for x in raw.split()]

    if len(outputs) < 3:
        print("Error: need at least 3 numbers.")
        return

    try:
        a, c = recover_lcg(outputs, m)
    except ValueError:
        print("Cannot invert (x2 - x1) mod m. Try different numbers.")
        return

    print(f"Recovered: a = {a}, c = {c}")

    ok = all((a * outputs[i] + c) % m == outputs[i + 1]
             for i in range(len(outputs) - 1))
    print("Matches all outputs:", ok)

    
    n = int(input("How many next values to predict? "))
    x = outputs[-1]
    for i in range(n):
        x = predict_next(x, a, c, m)
        print(f"Next {i + 1}: {x}")


if __name__ == "__main__":
    main()