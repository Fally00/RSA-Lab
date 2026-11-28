"""
app.py
Owner: Rayan
Purpose: Flask entry point: page routes (/, /audit, /keygen, /toolkit) and JSON API (/api/audit, /api/keygen, /api/toolkit).
"""
import json
import os
from flask import Flask, render_template, request, jsonify
from jinja2 import TemplateNotFound
import config

app = Flask(
    __name__,
    template_folder=os.path.join(config.BASE_DIR, "web", "pages"),
    static_folder=os.path.join(config.BASE_DIR, "web"),
    static_url_path="",
)
app.config["MAX_CONTENT_LENGTH"] = config.MAX_INPUT_CHARS * 2


ROUTES = {
    "index":   {"url": "/",        "label": "Landing"},
    "audit":   {"url": "/audit",   "label": "Audit"},
    "keygen":  {"url": "/keygen",  "label": "Keygen"},
    "toolkit": {"url": "/toolkit", "label": "Toolkit"},
}


def _mock():
    with open(config.MOCK_PATH, encoding="utf-8") as f:
        return json.load(f)


def _error(message, status=400):
    return jsonify({"error": message}), status


def _body():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def _page(name):
    """Render web/pages/<name>.html, or a stub if its owner hasn't pushed yet."""
    try:
        return render_template(f"{name}.html")
    except TemplateNotFound:
        links = [f'<a href="{route["url"]}">{route["label"]}</a>' for route in ROUTES.values()]
        nav = " | ".join(links)
        label = ROUTES[name]["label"]
        return (f"""<!doctype html>
<meta charset="utf-8">
<title>rsa-lab: {label}</title>
<body style="font-family:Georgia,serif;max-width:40rem;margin:4rem auto;padding:0 1rem">
  <h1>{label}</h1>
  <p>Template <code>web/pages/{name}.html</code> not pushed yet.</p>
  <p>{nav}</p>
</body>""")


def _stringify_key(key):
    return {k: (str(v) if isinstance(v, int) and not isinstance(v, bool) and k != "bits" and k != "actual_bits" else v)
            for k, v in key.items()}


def _run_toolkit_op(op, body):
    from core import gcd, modinv, modpow, solve_diophantine, crt
    from arith import euler_phi, carmichael_lambda, mobius_mu, sigma, tau
    from primality import miller_rabin, fermat_test

    if op == "gcd":
        a, b = int(body["a"]), int(body["b"])
        ans, steps = gcd(a, b, return_steps=True)
        return {"week": 2, "input": {"a": str(a), "b": str(b)}, "output": {"gcd": str(ans)}, "steps": steps}

    if op == "modinv":
        a, m = int(body["a"]), int(body["m"])
        ans, steps = modinv(a, m, return_steps=True)
        return {"week": 9, "input": {"a": str(a), "m": str(m)}, "output": {"inverse": str(ans)}, "steps": steps}

    if op == "modpow":
        base, exp, mod = int(body["base"]), int(body["exp"]), int(body["mod"])
        ans, steps = modpow(base, exp, mod, return_steps=True)
        return {"week": 9, "input": {"base": str(base), "exp": str(exp), "mod": str(mod)}, "output": {"result": str(ans)}, "steps": steps}

    if op == "diophantine":
        a, b, c = int(body["a"]), int(body["b"]), int(body["c"])
        res, steps = solve_diophantine(a, b, c, return_steps=True)
        out = {k: (str(v) if isinstance(v, int) and not isinstance(v, bool) else v) for k, v in res.items()}
        return {"week": 4, "input": {"a": str(a), "b": str(b), "c": str(c)}, "output": out, "steps": steps}

    if op == "crt":
        rems = [int(x) for x in body["remainders"]]
        mods = [int(x) for x in body["moduli"]]
        (x, M), steps = crt(rems, mods, return_steps=True)
        return {"week": 9, "input": {"remainders": [str(r) for r in rems], "moduli": [str(m) for m in mods]}, "output": {"x": str(x), "M": str(M)}, "steps": steps}

    if op == "arith_functions":
        n = int(body["n"])
        return {
            "week": 6,
            "input": {"n": str(n)},
            "output": {
                "phi": str(euler_phi(n)),
                "lambda": str(carmichael_lambda(n)),
                "mu": mobius_mu(n),
                "tau": str(tau(n)),
                "sigma": str(sigma(n)),
            },
            "steps": [f"Computed arithmetic functions for n = {n}."],
        }

    if op == "primality":
        n = int(body["n"])
        method = body.get("method", "miller_rabin")
        res = fermat_test(n) if method == "fermat" else miller_rabin(n)
        return {"week": 11, "input": {"n": str(n), "method": method}, "output": res, "steps": res.get("steps", [])}

    return None


# Flask routes for the web pages.

@app.get("/")
@app.get("/index.html")
def index():
    return _page("index")


@app.get("/audit")
@app.get("/audit.html")
def audit_page():
    return _page("audit")


@app.get("/keygen")
@app.get("/keygen.html")
def keygen_page():
    return _page("keygen")


@app.get("/toolkit")
@app.get("/toolkit.html")
def toolkit_page():
    return _page("toolkit")


# Flask routes for the JSON API.

@app.post("/api/audit")
def api_audit():
    text = _body().get("input")
    if not isinstance(text, str) or not text.strip():
        return _error('Send JSON like {"input": "<public keys>"}.')
    if len(text) > config.MAX_INPUT_CHARS:
        return _error(f"Input too long (max {config.MAX_INPUT_CHARS} chars).", 413)

    if config.USE_MOCK:
        mock = _mock()
        return jsonify({k: mock[k] for k in ("schema_version", "attack_registry", "keys", "batch", "report")})

    from audit.runner import run_audit
    try:
        return jsonify(run_audit(text))
    except ValueError as exc:
        return _error(str(exc), 400)


@app.post("/api/keygen")
def api_keygen():
    body = _body()
    bits = body.get("bits", config.DEFAULT_KEY_BITS)
    if isinstance(bits, bool) or not isinstance(bits, int) \
            or not config.MIN_KEY_BITS <= bits <= config.MAX_KEY_BITS:
        return _error(f"bits must be an integer from {config.MIN_KEY_BITS} to {config.MAX_KEY_BITS}.")

    exponent = body.get("exponent")
    try:
        exponent = int(exponent) if exponent not in (None, "") else None
        seed_text = body.get("seed", "")
        seed = None
        if seed_text:
            values = [int(value.strip()) for value in seed_text.split(",")]
            if len(values) != 2:
                raise ValueError("seed must be two comma-separated primes: p, q.")
            seed = values
    except (TypeError, ValueError):
        return _error("Enter a valid exponent and optional seed as p, q.")

    if config.USE_MOCK:
        return jsonify(_mock()["keygen"])

    from keygen import generate_strong_key, generate_weak_key
    kind = body.get("kind")
    try:
        if kind:
            weak = generate_weak_key(bits=bits, kind=kind)
            if isinstance(weak, tuple):
                return jsonify({"weak": [_stringify_key(k) for k in weak]})
            return jsonify({"weak": _stringify_key(weak)})
        strong = generate_strong_key(bits=bits, e=exponent, seed=seed)
        return jsonify({"strong": _stringify_key(strong)})
    except ValueError as exc:
        return _error(str(exc), 400)


@app.post("/api/toolkit")
def api_toolkit():
    body = _body()
    op = body.get("op")

    if config.USE_MOCK:
        toolkit = _mock()["toolkit"]
        if op not in toolkit:
            return _error(f"unknown toolkit operation '{op}'.")
        return jsonify(toolkit[op])

    try:
        result = _run_toolkit_op(op, body)
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        return _error(str(exc), 400)
    if result is None:
        return _error(f"unknown toolkit operation '{op}'.")
    return jsonify(result)


@app.get("/api/health")
def api_health():
    return jsonify({"ok": True, "mock": config.USE_MOCK})


@app.errorhandler(404)
def not_found(_):
    if request.path.startswith("/api/"):
        return _error("No such endpoint.", 404)
    return _page("index"), 404


# Run the Flask app.

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
