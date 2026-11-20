
## 2. [Omar Tarek]: Core Math Library

**Branch:** `[teeko]`
**Weeks:** W1, W2, W3, W4, W9
**Study:** divisibility, division algorithm, GCD and the Euclidean algorithm, Bézout's identity, linear Diophantine equations, congruences, modular inverse, fast modular exponentiation.

| Time | Task | Files |
|---|---|---|
| Nov 21-22 (2 d) | **Core v1, everyone depends on it:** `gcd`, `extended_gcd(a, b)` returning `(g, x, y)`, `modinv`, `modpow` (square-and-multiply), `isqrt`, `is_perfect_square` | `core/euclid.py`, `core/modular.py`, `core/roots.py` |
| Nov 23-24 (2 d) | `lcm`, `divides`, division algorithm (`q, r` with `0 ≤ r < d`), parity helpers | `core/divisibility.py`, `core/euclid.py` |
| Nov 25-26 (2 d) | `solve_diophantine(a, b, c)`: solvability check and general solution `x = x0 + (b/d)t`, `y = y0 - (a/d)t`; `crt(remainders, moduli)` | `core/diophantine.py`, `core/modular.py` |
| Nov 27-28 (2 d) | Make every function also return a step trace so the Toolkit page can show it; export everything | `core/__init__.py` |
| Dec 1-2 | ~60 s video segment and demo dry run | |

**Check your work:** compare against `math.gcd` and `pow(a, b, m)` in a scratch script.
