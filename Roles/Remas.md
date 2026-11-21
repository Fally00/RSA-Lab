# 8.[Remas]: Frontend Pages, Landing and Poster
 
**Branch:** `[name]` **Weeks:** W1-W9 (the Toolkit shows them), W14 (Keygen) 
 
You own the Keygen page, the Toolkit page, the landing page, `pages.css` (your page styles, so you never edit `style.css`) and the poster. Abdelrahman builds the foundation (layout, navbar, theme) on Nov 21, so start with wireframes. Build against `docs/mock_results.json`, do not wait for the backend. If it has no keygen or toolkit sample, ask Rayan.
 
**What the backend gives you** (outline; exact shapes are in `docs/mock_results.json`):
- `POST /api/keygen`: ask for `strong` or a weak kind (`small_primes`, `close_primes`, `small_d`, `shared_prime`) and a bit size, get back an `(n, e)` key
- `POST /api/audit`: send keys, get one report entry per key with the attack results. The Keygen page runs this on both keys
- `POST /api/toolkit`: send an operation name and numbers, get back `result` and `steps`

| Time | Task | Files |
|---|---|---|
| Nov 21-22 (2 d) | **Design first:** wireframes (paper, Figma or Excalidraw) of Keygen, Toolkit, landing and the poster using the theme below. Show Abdelrahman and Rayan, agree the Toolkit operation list with Rayan, then pull the foundation | no code yet |
| Nov 23-25 (3 d) | **Toolkit page:** operation picker (gcd, extended Euclid, modular inverse, modular exponentiation, Diophantine, CRT, φ(n), τ(n), σ(n), primality), input validation, the result with every step. From Nov 25 render steps with Abdelrahman's `explain_panel.html` | `templates/toolkit.html`, `js/toolkit.js`, `css/pages.css` |
| Nov 26-28 (3 d) | **Keygen page:** a weak key (kind picker) next to a strong key (bit size), both audited through `/api/audit` and shown with Abdelrahman's `result_card.html`. Attacks reveal one by one, ending with "0 of N attacks succeeded" on the strong key | `templates/keygen.html`, `js/keygen.js`, `css/pages.css` |
| Nov 29 (1 d) | **Landing page:** hero with a one-line pitch and an "Audit a key" button, a 3-step "how it works", feature cards with math symbols (Σ ≡ ∴ ∞) and week tags, a short "why not just ask an AI" block | `templates/index.html`, `web/static/img/` |
| Nov 30 - Dec 1 (2 d) | **Poster:** Problem → How number theory breaks weak keys → rsa-lab. Use the theme and screenshots of the Audit page and Explain mode. Everyone sends you 2-3 lines and one formula by Nov 29. The poster replaces your slides | `docs/poster/` |
| Dec 1-2 | ~60 s video segment and full demo dry run | |
 
During integration (Nov 27-29) test your pages against the real API as soon as Rayan has it running and report anything that breaks. Foundation, Audit and Explain files are Abdelrahman's: ask, don't edit.
 
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

 