
## 6. [Tamim]: Batch GCD, Reports + Extras

**Branch:** `[timo]`
**Weeks:** W2, W13, W14
**Study:** GCD in depth, hash functions, random number generation (LCGs, seeds, entropy), basics of the Digital Signature Standard.

| Time | Task | Files |
|---|---|---|
| Nov 21-23 (3 d) | `run_batch(keys)`: `gcd(n_i, n_j)` for every pair; a result above 1 breaks both keys (use `math.gcd` until Core v1 lands) | `attacks/shared_prime.py` |
| Nov 24-25 (2 d) | SHA-256 fingerprint of each audit report | `report/fingerprint.py`, `report/__init__.py` |
| Nov 26-27 (2 d) | *Optional upgrade:* product-tree batch gcd so it scales to thousands of keys | `attacks/shared_prime.py` |
| Nov 28-29 (2 d) | *Stretch:* LCG predictor, recover the generator's parameters from its outputs | `extras/lcg_predictor.py` |
| Dec 1-2 | ~60 s video segment and demo dry run | |

**Check your work:** a known shared-prime pair must be detected (Member 5's `weak_keys.py` provides one from Nov 24).
**If you finish early:** `extras/dsa_nonce.py` (DSA nonce-reuse private key recovery, W14) is the next stretch. No fixed date.
