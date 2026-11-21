# 7.[Abdelrahman]: Frontend Core (foundation, Audit page, Explain mode)
 
**Branch:** `3r3r` 
**Weeks:** W10 (timing visuals)
 
You own the foundation every page stands on, plus the two screens the demo lives in: the Audit page and Explain mode. Member 8 builds on your foundation, so it ships first. Build against `docs/mock_results.json` from day one, do not wait for the backend.
 
**What the backend gives you** (outline; exact shapes are in `docs/mock_results.json`):
- `POST /api/audit`: send keys, get one report entry per key with the attack results and a report fingerprint
- `POST /api/keygen`: ask for `strong` or a weak kind (`small_primes`, `close_primes`, `small_d`, `shared_prime`), get back an `(n, e)` key. Powers "Load demo keys"

| Time | Task | Files |
|---|---|---|
| Nov 21 (1 d) | **Foundation:** base layout, navbar, theme toggle (dark and light), CSS variables from the theme below, shared fetch helper. Push today, Member 8 builds on it | `web/templates/base.html`, `partials/navbar.html`, `css/style.css`, `js/api.js` |
| Nov 22-23 (2 d) | **Audit page (the main screen):** paste or upload keys, "Load demo keys" button, loading and error states, summary banner (scanned / broken), one verdict card per key with factors and recovered private key (copy button), report fingerprint, "Download report" (JSON). Push `result_card.html` by Nov 23, Member 8 reuses it | `templates/audit.html`, `partials/result_card.html`, `js/audit.js` |
| Nov 24-25 (2 d) | **Explain mode:** step-by-step viewer (next / back / play) over an attack's steps, table rendering (Wiener's convergents), week tags (W5, W12...), a short "why this works" blurb per attack. Push by Nov 25, Member 8 reuses it | `partials/explain_panel.html`, `js/explain.js`, `css/explain.css` |
| Nov 26-27 (2 d) | **Timing chart:** bar chart of `time_ms` per attack on the audit page, colored from the theme variables | `js/charts.js`, `js/vendor/` (local `chart.min.js`) |
| Nov 28-29 (2 d) | **Integration:** switch to the real API (Rayan has it from Nov 27), test with 100-digit numbers, empty and error states, small screens | your files |
| Nov 30 (1 d) | 1-2 slides on the frontend | `docs/slides/abdelrahman.md` |
| Dec 1-2 | ~60 s video segment and full demo dry run | |
 
#### Keygen, Toolkit, landing and `pages.css` are Remas's: ask, don't edit.
 
## Theme (same in both files)
 
Feel: a modern mathematical journal mixed with an interactive learning platform. Editorial typography, matte surfaces, subtle borders, restrained color, real mathematical illustrations instead of random decoration, plenty of whitespace in light mode, layered charcoal in dark mode.
 
| Token | Dark | Light | Use |
|---|---|---|---|
| `--bg` | `#111113` | `#F5F2EE` | Page |
| `--surface` | `#1A191B` | `#FFFFFF` | Cards |
| `--elevated` | `#242225` | `#EAE5DF` | Raised or hovered |
| `--text` | `#EAE5E1` | `#171619` | Primary text |
| `--text-2` | `#AAA3A0` | `#77716E` | Secondary text |
| `--accent` | `#963B45` | `#963B45` | Burgundy: buttons (white text), active nav, key math elements. Use sparingly |
| `--accent-text` (added) | `#D9737F` | `#963B45` | Links and highlighted words, since plain burgundy is too dark for text on dark |
| `--border` (added) | `#2E2C2F` | `#DDD7D0` | Subtle borders |
| `--safe` (added) | `#7DBE98` | `#2E6B4E` | Safe key |
 
