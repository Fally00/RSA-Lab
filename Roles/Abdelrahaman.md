
## 7. [Abdelrahman]: Frontend (the whole `web/` folder)

**Branch:** `[3r3r]`
**Weeks:** W10 (timing visuals), plus a skim of all weeks so labels and explanations are correct
**Study:** Flask templates (Jinja), JavaScript `fetch`, Chart.js, and a high-level read of what each attack does.

You own everything the browser shows. It is what the doctor sees in the demo and the video, so treat it like a product, not a form. **Build against `docs/mock_results.json` from day one, do not wait for the backend.**

**What the backend gives you** (outline; exact shapes are in `docs/mock_results.json`):
- `POST /api/audit`: send keys, get one report entry per key with the list of attack results (see the contract in the README) and a report fingerprint
- `POST /api/keygen`: ask for `strong` or a weak kind (`small_primes`, `close_primes`, `small_d`, `shared_prime`), get back an `(n, e)` key
- `POST /api/toolkit`: send an operation name and numbers, get back `result` and `steps`

| Time | Task | Files |
|---|---|---|
| Nov 21 (1 d) | **Design foundation:** base layout, navbar, theme (dark and light, readable on a projector), shared fetch helper | `web/templates/base.html`, `partials/navbar.html`, `css/style.css`, `js/api.js` |
| Nov 22-23 (2 d) | **Audit page (the main screen):** paste or upload keys, a "Load demo keys" button, loading and error states, summary banner (keys scanned / broken), one 🟢/🔴 card per key with factors and recovered private key (copy button), report fingerprint, "Download report" (JSON) | `templates/audit.html`, `partials/result_card.html`, `js/audit.js` |
| Nov 24-25 (2 d) | **Explain mode:** step-by-step viewer (next / back / play) over an attack's `steps`, table rendering (Wiener's convergents), week tags (W5, W12...), a short "why this works" blurb per attack | `partials/explain_panel.html`, `js/explain.js`, `css/explain.css` |
| Nov 26-27 (2 d) | **Keygen page and timing chart:** generate a strong key next to a weak one, audit both, show every attack failing on the strong one. Bar chart of `time_ms` per attack (W10) | `templates/keygen.html`, `js/keygen.js`, `js/charts.js`, `js/vendor/` (local `chart.min.js`) |
| Nov 28-29 (2 d) | **Toolkit page:** pick an operation (gcd, extended Euclid, modular inverse, Diophantine, φ(n)...), enter numbers, see the result with every step | `templates/toolkit.html`, `js/toolkit.js` |
| Nov 30 - Dec 1 (2 d) | **Landing page, final polish** (empty states, small screens, logo) and the **poster** (Problem → How number theory breaks weak keys → rsa-lab). Others send you content. The poster replaces your slides | `templates/index.html`, `web/static/img/`, `docs/poster/` |
| Dec 2 | Full demo dry run | |

During integration (Nov 27-29) test your pages against the real API as soon as Rayan has it running and report anything that breaks.
