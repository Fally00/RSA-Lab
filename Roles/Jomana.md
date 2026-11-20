
## 4. [Jomana]: Wiener Attack + Number-Theory Functions

**Branch:** `[jomana]`
**Weeks:** W5, W6, W7
**Study:** continued fractions and convergents, Wiener's theorem (works when `d < n^(1/4) / 3`), the functions τ(n), σ(n), s(n), φ(n), λ(n) (Carmichael), μ(n), multiplicative functions.

| Time | Task | Files |
|---|---|---|
| Nov 21-22 (2 d) | Continued fraction expansion and convergents of a rational | `arith/continued_fractions.py` |
| Nov 23-25 (3 d) | `run(n, e)`: expand `e/n`, test each convergent `k/d`, compute candidate `φ = (e·d - 1) / k`, solve the quadratic for `p, q`. Put the **convergents table** in `steps` | `attacks/wiener.py` |
| Nov 26 (1 d) | `run(n, e, phi=None, sigma=None)`: if φ known then `p + q = n - φ + 1`; if σ known then `p + q = σ - n - 1`; solve `x² - (p+q)x + n = 0` | `attacks/phi_leak.py` |
| Nov 27-28 (2 d) | `tau`, `sigma`, `s`, `phi`, `carmichael_lambda`, `mobius` for small `n`, each with a step trace (the Toolkit page shows them) | `arith/arith_functions.py`, `arith/totient.py`, `arith/__init__.py` |
| Nov 29 (1 d) | *Bonus:* Pell's equation solver using continued fractions | `arith/pell.py` |
| Dec 1-2 | ~60 s video segment and demo dry run | |

**Check your work:** a key with a deliberately small `d` (Wiener must recover it) and a hardened key (Wiener must fail).
