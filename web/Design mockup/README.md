# Number Theory — refined frontend handoff

This package contains a cleaned-up four-page visual prototype based on the supplied Stitch export.

## Files
- `index.html` — Home (`/`)
- `audit.html` — Audit (`/audit`)
- `keygen.html` — Keygen (`/keygen`)
- `toolkit.html` — Toolkit (`/toolkit`)
- `styles.css` — Shared design system and responsive layout
- `app.js` — Theme switching, mobile navigation, tab behavior and safe local preview calculations
- `DESIGN.md` — Design tokens, component rules and implementation notes

## Run locally
Open `index.html` in a browser, or serve this folder with any static HTTP server.

## Design decisions
- Retains the sculptural editorial direction, Playfair Display / DM Sans / DM Mono typography, matte charcoal, warm ivory and restrained burgundy.
- Defaults to dark mode; the theme toggle switches both themes and stores the preference in local storage.
- Uses one shared navigation and footer across all four pages.
- Desktop-first layout, with mobile adaptation and no persistent bottom navigation.
- Removes fabricated institutional branding, ISSNs, archival references, fake research metrics, unsupported security guarantees and ornamental system metadata.
- Avoids adding routes beyond the four supplied application pages.

## Backend integration notes
This is a frontend handoff prototype, not a replacement for the Flask application.
- Map the four HTML files to the existing Flask routes: `/`, `/audit`, `/keygen`, `/toolkit`.
- `audit.html` contains a small safe-integer browser preview for primality, factorization and GCD. Replace or supplement it with the actual `/audit` backend contract.
- `keygen.html` intentionally does not generate keys in the browser. Connect its fields to the existing `/keygen` endpoint and display only backend-generated key material.
- `toolkit.html` includes local previews for modular exponentiation and GCD. Connect the remaining tools to confirmed backend operations.
- Preserve server-side validation, cryptographic randomness, key handling and error reporting. Do not trust client-side values as authoritative.

## Known limitations
- The homepage sculpture image is referenced from the original Stitch-hosted image URL. Replace it with a locally licensed project asset before production if the URL is not suitable for deployment.
- The prototype does not include the Flask backend, authentication, persistence of calculations, or production cryptographic operations.
