
## 3. [Basuony]: Factoring Attacks

**Branch:** `[beso]`
**Weeks:** W3, W10, W12
**Study:** Fundamental Theorem of Arithmetic, why you only need to test up to √n, Fermat factorization (difference of squares, works when `p` and `q` are close), Pollard's rho (cycle detection), computational complexity and why factoring is hard.

| Time | Task | Files |
|---|---|---|
| Nov 21-22 (2 d) | `run(n, e)`: try divisors up to a limit, record each step. After finding `p, q` compute `φ = (p-1)(q-1)` and `d = e⁻¹ mod φ` | `attacks/trial_division.py` |
| Nov 23-24 (2 d) | `run(n, e)`: search `a` from `⌈√n⌉` until `a² - n` is a perfect square | `attacks/fermat.py` |
| Nov 25-26 (2 d) | `run(n, e)`: Floyd cycle detection with `f(x) = x² + c mod n` | `attacks/pollard_rho.py` |
| Nov 27-28 (2 d) | W10: make sure `time_ms` is measured the same way in all three attacks, write up why their speeds differ, and help Rayan with integration bugs | |
| Dec 1-2 | ~60 s video segment and demo dry run | |

**Check your work:** a key with close primes (Fermat should win) and a key with a small factor (trial division should win). Member 5's `weak_keys.py` will give you these from Nov 24.