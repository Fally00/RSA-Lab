
## 5. [Haneen]: Primality + Hardened Keygen

**Branch:** `[haneen]`
**Weeks:** W8, W11, W14
**Study:** distribution of primes (density about `1/ln n`), Fermat primality test, Carmichael numbers (why Fermat alone is not enough), Miller-Rabin, RSA key generation, public-key cryptography.

| Time | Task | Files |
|---|---|---|
| Nov 21-22 (2 d) | Fermat primality test and Miller-Rabin (record each witness in `steps`) | `primality/fermat_test.py`, `primality/miller_rabin.py`, `primality/__init__.py` |
| Nov 23-24 (2 d) | `generate_prime(bits)` and the **demo weak keys**: `small_primes`, `close_primes`, `small_d`, plus a **pair of keys that share a prime**. Push early: Members 3, 4, 6 and 7 test and demo with these | `keygen/generate.py`, `keygen/weak_keys.py`, `keygen/__init__.py` |
| Nov 25-26 (2 d) | `generate_strong_key(bits)`: `p, q` far apart, `e = 65537`, `gcd(e, φ) = 1`, `d` via modular inverse. And `run(n, e)`: flags `n` that is prime (then `φ = n - 1`), a perfect square (`p = q`), or even | `keygen/generate.py`, `attacks/bad_modulus.py` |
| Nov 27-28 (2 d) | Prime density experiment: tries needed to find a prime vs the `1/ln n` prediction (W8) | `primality/density.py` |
| Dec 1-2 | ~60 s video segment and demo dry run | |

**Check your work:** Miller-Rabin must accept known primes, reject composites, and catch Carmichael numbers like 561 that fool the Fermat test.
