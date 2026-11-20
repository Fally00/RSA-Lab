# Team Roles

**Before you start:** read sections 6 (Project structure) and 7 (Shared contract) in [`README.md`](README.md). Every file already exists with a header comment. **Only edit the files listed under your name.**

**Done means:**
1. Follows the shared contract
2. Works on a few small toy keys you can verify by hand (`p × q = n`)
3. `steps` is readable for Explain mode
4. Pushed on your branch, ready to merge

---

## Team Members

-> See [Roles](Roles/) for each member role there is a markdown file to read
- [Rayan](Roles/Rayan.md)
- [Omar_Tarek](Roles/Omar_Tarek.md)
- [Basouny](Roles/Basouny.md)
- [Jomana](Roles/Jomana.md)
- [Haneen](Roles/Haneen.md)
- [Tamim](Roles/Tamim.md)
- [Abdelrahman](Roles/Abdelrahaman.md)

---

## Section 6.Project structure


The skeleton is already created: every file exists with a header comment saying who owns it and what it is for. **Fill in your own files only.**

```
rsa-lab/
│
├── app.py                      # Flask entry point: page routes + JSON API (/api/audit, /api/keygen, /api/toolkit)   [Rayan]
├── config.py                   # Settings: default key size, attack time limits           [Rayan]
├── requirements.txt            # Python dependencies                                      [Rayan]
├── .gitignore                  # Files git should ignore (venv, __pycache__, ...)         [Rayan]
├── README.md                   
├── ROLES.md                    # Who builds what, which files, and when
│
├── audit/                      # The "brain" that runs everything                         [Rayan]
│   ├── __init__.py
│   ├── parser.py               # Turns PEM keys / raw "n, e" text into (n, e) pairs
│   ├── runner.py               # Calls every registered attack on each key, merges results
│   └── contract.py             # Builds and validates the shared result dict
│
├── core/                       # Math library everything else builds on                   [Omar tarek]
│   ├── __init__.py
│   ├── divisibility.py         # W1: divides check, division algorithm, parity helpers
│   ├── euclid.py               # W2: gcd, lcm, extended_gcd (with step trace)
│   ├── diophantine.py          # W4: solvability test + general solution of ax + by = c
│   ├── modular.py              # W9: modinv, modpow (square-and-multiply), crt
│   └── roots.py                # integer square root, perfect-square test
│
├── attacks/                    # One file per attack, all follow the shared contract
│   ├── __init__.py             # Registry: the list of attacks the runner calls           [Rayan  ]
│   ├── trial_division.py       # W3: try small divisors up to √n                          [Basouny]
│   ├── fermat.py               # W12: Fermat factorization (close primes)                 [Basouny]
│   ├── pollard_rho.py          # W12: Pollard's rho factoring                             [Basouny]
│   ├── wiener.py               # W5: small-d attack via continued fractions               [Jomana ]
│   ├── phi_leak.py             # W6/W7: recover p, q when φ(n) or σ(n) is known           [Jomana ]
│   ├── bad_modulus.py          # W11: n prime, n a perfect square, n even                 [Haneen ]
│   └── shared_prime.py         # W2: batch gcd across many keys                           [Tamim  ]
│
├── arith/                      # Number-theory functions: continued fractions (Wiener needs them), [Jomana]
│   │                           # τ/σ/φ/λ/μ and Pell. Mostly feeds the Toolkit page and slides
│   ├── __init__.py
│   ├── continued_fractions.py  # W5: expansion and convergents (used by wiener.py)
│   ├── arith_functions.py      # W6: τ(n), σ(n), s(n)
│   ├── totient.py              # W7: φ(n), Carmichael λ(n), μ(n)
│   └── pell.py                 # W5 bonus: Pell's equation
│
├── primality/                  # Is this number prime?                                    [Haneen]
│   ├── __init__.py
│   ├── fermat_test.py          # W11: Fermat primality test
│   ├── miller_rabin.py         # W11: Miller-Rabin with witness trace
│   └── density.py              # W8: tries needed to find a prime vs 1/ln(n)
│
├── keygen/                     # Making keys                                              [Haneen]
│   ├── __init__.py
│   ├── generate.py             # generate_prime(bits) and generate_strong_key(bits)
│   └── weak_keys.py            # demo weak keys: small primes, close primes, small d, shared prime
│
├── report/                     # Audit report integrity                                   [Tamim]
│   ├── __init__.py
│   └── fingerprint.py          # W13: SHA-256 fingerprint of each audit report
│
├── extras/                     # STRETCH goals, standalone, not wired into the audit      [Tamim]
│   ├── lcg_predictor.py        # W13: predict an LCG random generator from its outputs
│   └── dsa_nonce.py            # W14: DSA nonce-reuse private key recovery
│
├── web/                        # Everything the browser sees (the whole frontend)         [Abdelrahamn]
│   ├── templates/              # HTML pages (Jinja, rendered by Flask)
│   │   ├── base.html           # Shared layout: head, navbar, footer, script tags
│   │   ├── index.html          # Landing page: what rsa-lab is + how it works
│   │   ├── audit.html          # Main page: paste keys, run audit, results, timing view
│   │   ├── keygen.html         # Generate a hardened key and audit it next to a weak one
│   │   ├── toolkit.html        # Math toolkit: calculator with every step shown
│   │   └── partials/           # Small reusable HTML blocks
│   │       ├── navbar.html
│   │       ├── result_card.html    # One 🟢/🔴 verdict card
│   │       └── explain_panel.html  # Step-by-step viewer for an attack's "steps" (Explain mode)
│   └── static/                 # Files served as-is by Flask
│       ├── css/
│       │   ├── style.css       # Global theme (dark + light) and layout
│       │   └── explain.css     # Styling for Explain mode panels and tables
│       ├── js/
│       │   ├── api.js          # Shared helper for calling the /api endpoints
│       │   ├── audit.js        # Sends keys to /api/audit, renders results
│       │   ├── explain.js      # Builds the step-by-step trace view
│       │   ├── keygen.js       # Keygen page logic
│       │   ├── toolkit.js      # Toolkit page logic
│       │   ├── charts.js       # Chart.js helpers (attack timing bars)
│       │   └── vendor/         # Third-party libs (drop chart.min.js here)
│       └── img/                # Logo, icons, poster images
│
└── docs/
    ├── mock_results.json       
    ├── poster/                
    ├── slides/                 
    └── video/         
```

---

## Section 7.Shared contract

Every attack is a function `run(n, e)` that returns a dict with these keys:

```python
{
    "attack": "fermat",     # name
    "week": 12,             # syllabus week
    "broken": True,         # did it break the key?
    "factors": [p, q],      # None if it failed
    "private_key": d,       # None if it failed
    "steps": ["..."],       # readable trace for Explain mode
    "time_ms": 1.7,         # how long it took
}
```

Rules:
1. If the attack fails: `broken: False`, `factors` and `private_key` are `None`, and still fill `steps` with what it tried.
2. A table (e.g. Wiener's convergents) goes inside `steps` as `{"table": {"headers": [...], "rows": [[...]]}}`.
3. Never `print()`. Return everything in the dict.
4. Batch attacks (shared prime) use `run_batch(keys)` and return one dict per key.

`audit/contract.py` has a helper that builds this dict, and `docs/mock_results.json` shows a full example.

---

## Weeks coverage check

| Week | Topic | Owner |
|---|---|---|
| 1 | Divisibility | 2 |
| 2 | GCD, Euclid | 2, 6 |
| 3 | FTA, primes | 2, 3 |
| 4 | Diophantine | 2 |
| 5 | Continued fractions, Pell | 4 |
| 6 | τ, σ, s | 4 |
| 7 | φ, λ, μ | 4 |
| 8 | Prime distribution | 5 |
| 9 | Congruences | 2 |
| 10 | Complexity (attack timing view) | 3, 7 |
| 11 | Primality testing | 5 |
| 12 | Factorization | 3 |
| 13 | Hashes (report fingerprint), RNG (stretch LCG) | 6 |
| 14 | Public-key crypto (keygen), DSS (stretch) | 5, 6 |

## Presentation and video split

- Presentaion with transitions and effects [Basouny]
- Video making [Rayan]
- video editing [Omar Tarek]
- poster [Tamim]