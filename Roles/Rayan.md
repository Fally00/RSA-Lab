## 1. Rayan: Team Lead / Integration

**Branch:** `rayo`
**Study:** W1-W2 refresher, W9 (congruences), W14 (how RSA works end to end), plus a skim of every other member's weeks so integration makes sense.

| Time | Task | Files |
|---|---|---|
| Nov 21 (1 d) | Put the contract in code and write fake results so Member 7 can start immediately | `audit/contract.py`, `docs/mock_results.json` |
| Nov 21-23 (3 d) | Flask app: pages `/`, `/audit`, `/keygen`, `/toolkit` and JSON endpoints `/api/audit`, `/api/keygen`, `/api/toolkit` (return mock data at first) | `app.py`, `config.py`, `requirements.txt`, `.gitignore` |
| Nov 24-25 (2 d) | Key parser: PEM public keys (using the `cryptography` library) and raw `n, e` text | `audit/parser.py` |
| Nov 26-27 (2 d) | Runner and registry: call every attack on each key, merge results into one report | `audit/runner.py`, `attacks/__init__.py` |
| Nov 22-29 | Review and merge every branch as it becomes ready | |
| Nov 27-29 (3 d) | Integration: swap mock data for the real attacks, fix what breaks | everything |
| Nov 30 (1 d) | Merge everyone's slides into the final deck | `docs/slides/` |
| Dec 2 | Full demo dry run | |
