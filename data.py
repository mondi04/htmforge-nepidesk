"""
htmforge-demo — data.py
Statische Inhalte für die Landing Page.
"""

HTMFORGE_VERSION = "0.4.0"
SITE_URL         = "https://htmforge.nepidesk.de"

# ── Hero ──────────────────────────────────────────────────
HERO_CLAIM = "HTML. In Python. Ohne Templates."
HERO_SUB   = (
    "htmforge ist eine Python-Bibliothek für typsicheres HTML-Rendering — "
    "kein Jinja, kein Template-Ordner, keine String-Concatenation. "
    "Jedes Element ist eine Python-Funktion."
)

# ── Konzept-Punkte ────────────────────────────────────────
CONCEPTS = [
    {
        "num":   "01",
        "title": "Kein Template-Engine",
        "desc":  (
            "Jinja, Mako, Chameleon — alle lösen dasselbe Problem mit dem gleichen Ansatz: "
            "Strings mit Platzhaltern. htmforge bricht damit. HTML entsteht direkt in Python, "
            "in derselben Datei, mit denselben Tools."
        ),
    },
    {
        "num":   "02",
        "title": "Typsicher & composable",
        "desc":  (
            "Jede Funktion gibt ein validiertes Element zurück. Attribute werden geprüft, "
            "XSS-Escaping übernimmt markupsafe automatisch. Komponenten sind einfach "
            "Python-Funktionen — testbar, wiederverwendbar, refactorable."
        ),
    },
    {
        "num":   "03",
        "title": "Für den Server gedacht",
        "desc":  (
            "Kein Build-Step, kein npm, kein Webpack. htmforge rendert serverseitig — "
            "ideal für Flask, FastAPI oder jede andere WSGI/ASGI-App. "
            "Perfekt kombinierbar mit HTMX für partielle Updates."
        ),
    },
]

# ── Code-Beispiele ────────────────────────────────────────
CODE_EXAMPLES = [
    {
        "title":  "Einfaches Element",
        "desc":   "Ein Button — fertig in einer Zeile.",
        "code":   """\
from htmforge.elements import button

result = button("Speichern", class_="btn-primary", type="submit")
# → <button class="btn-primary" type="submit">Speichern</button>""",
        "output": '<button class="btn-primary" type="submit">Speichern</button>',
    },
    {
        "title":  "Komponente als Funktion",
        "desc":   "Wiederverwendbare UI-Bausteine — einfach Python-Funktionen.",
        "code":   """\
from htmforge.elements import div, span, p

def status_badge(label: str, online: bool):
    color = "green" if online else "red"
    return div(
        span("●", class_=f"dot dot-{color}"),
        span(label, class_="badge-label"),
        class_="status-badge",
    )

result = status_badge("Server A", online=True)
# → <div class="status-badge">
#     <span class="dot dot-green">●</span>
#     <span class="badge-label">Server A</span>
#   </div>""",
        "output": (
            '<div class="status-badge">'
            '<span class="dot dot-green">●</span>'
            '<span class="badge-label">Server A</span>'
            '</div>'
        ),
    },
    {
        "title":  "Ganze Seite in Python",
        "desc":   "Eine vollständige HTML-Seite — kein Template-Ordner, keine .html-Datei.",
        "code":   """\
from htmforge import render
from htmforge.elements import html, head, body, title, h1, p

page = html(
    head(title("Meine Seite")),
    body(
        h1("Hallo Welt"),
        p("Gebaut mit htmforge."),
    ),
    lang="de",
)

output = "<!DOCTYPE html>\\n" + render(page)""",
        "output": (
            "<!DOCTYPE html>\n"
            '<html lang="de">'
            "<head><title>Meine Seite</title></head>"
            "<body><h1>Hallo Welt</h1><p>Gebaut mit htmforge.</p></body>"
            "</html>"
        ),
    },
]

# ── Install ───────────────────────────────────────────────
INSTALL_CMD = f"pip install htmforge=={HTMFORGE_VERSION}"
PYPI_URL    = "https://pypi.org/project/htmforge/"
GITHUB_URL  = "https://github.com/mondi04/htmforge"

# ── Demo-Beschreibung ─────────────────────────────────────
DEMO_INTRO = {
    "title":   "Live Demo — User Management",
    "desc": (
        "Die folgende Admin-UI ist vollständig mit htmforge gebaut — "
        "kein Jinja, keine .html-Dateien. Dashboard, Tabelle, Formulare: "
        "alles Python-Funktionen, alles serverseitig gerendert."
    ),
    "url":     "/demo",
    "cta":     "Demo öffnen →",
}