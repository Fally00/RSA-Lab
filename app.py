"""
app.py
Owner: Rayan
Purpose: Flask entry point: page routes (/, /audit, /keygen, /toolkit) and JSON API (/api/audit, /api/keygen, /api/toolkit).
"""
import json
from flask import Flask, render_template, request, jsonify
from jinja2 import TemplateNotFound
import config

app = Flask(__name__ , template_folder="web/templates", static_folder="web/static")
app.config["MAX_CONTENT_LENGHT"] = config.MAX_INPUT_CHARS *2


ROUTES = {
    "index":   {"url": "/",        "label": "Landing"},
    "audit":   {"url": "/audit",   "label": "Audit"},
    "keygen":  {"url": "/keygen",  "label": "Keygen"},
    "toolkit": {"url": "/toolkit", "label": "Toolkit"},
}

# Render web/templates/<name>.html, or a stub if its owner hasn't pushed yet.
# Use Mock data for the JSON API if config.MOCK_PATH is set, otherwise call the real function.

def _mock():

    with open(config.MOCK_PATH , encoding = "utf-8") as f:
        return json.load(f)

def _error(message , status = 400):
    return jsonify({"error" : message}) , status

def _body():
    data = request.get_json(silent=True)
    return data if isinstance(data , dict) else {}

def _page(name):
    """Render web/templates/<name>.html, or a stub if its owner hasn't pushed yet."""
    try:
        return render_template(f"{name}.html")
    except TemplateNotFound:
        links = []
        for route in ROUTES.values():
            links.append(f'<a href="{route["url"]}">{route["label"]}</a>')
        nav = " | ".join(links)
        label = ROUTES[name]["label"]

        return (f"""<!doctype html>
<meta charset="utf-8">
<title>rsa-lab: {label}</title>
<body style="font-family:Georgia,serif;max-width:40rem;margin:4rem auto;padding:0 1rem">
  <h1>{label}</h1>
  <p>Template <code>web/templates/{name}.html</code> not pushed yet.</p>
  <p>{nav}</p>
</body>""")

# Flask routes for the web pages.
@app.get("/")
def index():
    return _page("index")


@app.get("/audit")
def audit_page():
    return _page("audit")


@app.get("/keygen")
def keygen_page():
    return _page("keygen")


@app.get("/toolkit")
def toolkit_page():
    return _page("toolkit")

