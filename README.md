# rsa-lab

> An offline RSA audit lab. It finds weak keys, **proves** they are broken by handing back the factors, shows step by step *why* each attack worked, and generates hardened keys that survive the same audit.

Course project for **BS 208 – Elementary Number Theory** (Cyber Security, Section A2).
Deadline: **before December 3**. Team of 7. See [`instructions.md`](Roles/Instructions.md) for who builds what and when.

---

## 1. The problem

RSA fails **silently**. A weak key looks identical to a strong one until someone factors it, and the usual causes are all number-theory mistakes:

- primes that are too small or too close together
- two keys that accidentally share a prime (bad random number generator)
- a private exponent `d` that is too small
- a "prime" that is not actually prime (buggy generator)

Nothing warns you before an attacker finds out.

## 2. Our solution

A local web app (Flask + Python big integers) that works as an **attacker's-view audit**:

1. You paste RSA public keys (PEM or raw `n, e`).
2. The app runs every known cheap attack on them.
3. Each verdict is backed by **verifiable proof** (`p × q = n`, recovered private key) and a **step-by-step trace** tagged with the course week.
4. A hardened key generator builds keys that resist all of these attacks, then audits them live to show every attack fail.

Why not just ask an AI? Language models cannot reliably factor numbers or run continued-fraction expansions. Python can, and the output is checkable. The tool also runs offline, is repeatable, and can scan many keys in bulk (batch gcd), which a chat window cannot.

## 3. Features

| Module | What it does | Course weeks |
|---|---|---|
| **Audit** | Runs all attacks on pasted keys, gives 🟢 / 🔴 verdict with proof | all |
| **Explain mode** | Shows the math trace behind every result (gcd chain, convergents table, Fermat steps) | all |
| **Factoring attacks** | Trial division, Fermat, Pollard rho | W3, W12 |
| **Wiener attack** | Recovers a small `d` using continued fractions | W5 |
| **φ / σ leak check** | If φ(n) or σ(n) leaks, recover `p` and `q` with a quadratic | W6, W7 |
| **Bad-modulus check** | Miller-Rabin on `n`, perfect-square and even checks | W11 |
| **Batch gcd** | Finds shared primes across many keys | W2 |
| **Hardened keygen** | Builds keys resistant to every attack, then proves it by auditing them | W11, W14 |
| **Attack timing view** | Every attack reports `time_ms`; the app shows them side by side | W10 |
| **Math toolkit** | Interactive calculator (gcd, extended Euclid, Diophantine, modular inverse, φ(n), τ(n), σ(n)...) with every step shown | W1-W9 |
| **Report fingerprint** | SHA-256 fingerprint of every audit report | W13 |
| **Core math library** | gcd, extended Euclid, modular inverse, modular exponentiation, Diophantine, CRT | W1-W4, W9 |

**Stretch goals (only if ahead):** LCG predictor (W13), DSA nonce-reuse attack (W14), Pell's equation (W5).

**Not included for now:** fleet simulator, automated tests, benchmark / attack-race chart. They can be added later.

## 4. Honest limits

- A properly generated 2048-bit RSA key will **not** break. That is the point of the "hardened" side of the app.
- Tools like RsaCtfTool and badkeys already exist. Ours is different because it is educational (explain mode, math toolkit), covers the whole syllabus, and includes the fix side.
- Educational use only. Audit keys you generated yourself or toy keys. Do not use it against systems you do not own.

## 5. Tech stack

- Python 3.12+
- Flask (backend and templates)
- HTML / CSS / vanilla JS, Chart.js for graphs
- `cryptography` library **only** for parsing PEM keys
- No hosting, runs on `localhost`
- Github Actions extenion on VS code
- for github tutorial check [Github_tutorial](https://youtu.be/N7qWNQxFq90)

**Rule:** implement the number theory yourself. Do not call `sympy.factorint`, `sympy.isprime`, etc. for the real code. You may use them in a scratch script to check your answers. Python's built-in `math.gcd` and `pow(a, b, m)` are fine as references to compare against.

## 6. Project structure

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

**How a request flows:** browser page (`web/`) → `fetch` to an `/api/...` route in `app.py` → `audit/runner.py` → each file in `attacks/` (which use `core/`, `arith/`, `primality/`) → result dicts → back to the page, which draws them. The Toolkit page skips the runner and calls `core/` and `arith/` directly through `/api/toolkit`.

## 7. Shared contract

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

## 8. Deliverables

- **Application:** this repo, running on localhost
- **Presentation:** each member prepares 1-2 slides on their module (`docs/slides/<name>.md`), Rayan merges them
- **Poster:** Problem → How number theory breaks weak keys → rsa-lab (`docs/poster/`)
- **Video (~10 min):** intro + one short segment per member + live demo (paste 3 keys, crack two, show a hardened key survive)

## 9. Team

-> See [Roles](Roles/) for each member role there is a markdown file to read
- [Rayan](Roles/Rayan.md)
- [Omar_Tarek](Roles/Omar_Tarek.md)
- [Basouny](Roles/Basouny.md)
- [Jomana](Roles/Jomana.md)
- [Haneen](Roles/Haneen.md)
- [Tamim](Roles/Tamim.md)
- [Abdelrahman](Roles/Abdelrahaman.md)

#### Follow [instructions](Roles/Instructions.md)