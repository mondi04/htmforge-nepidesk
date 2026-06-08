"""
htmforge-demo — components.py
Alle UI-Komponenten. Landing Page + Admin Demo.
"""

from htmforge import render
from htmforge.elements import (
    div, span, a, p, h1, h2, h3, nav, header, footer,
    main, section, form, input, label, select, option,
    script, link, meta, html, head, body, title,
    button, table, thead, tbody, tr, th, td, raw,
    textarea,
)

from data import (
    HTMFORGE_VERSION, SITE_URL,
    HERO_CLAIM, HERO_SUB,
    CONCEPTS, CODE_EXAMPLES,
    INSTALL_CMD, PYPI_URL, GITHUB_URL,
    DEMO_INTRO,
    IMPRESSUM, DATENSCHUTZ,
)


# ── Head ──────────────────────────────────────────────────

def _head(page_title: str, description: str, css_hash: str = ""):
    return head(
        meta(charset="UTF-8"),
        meta(name="viewport", content="width=device-width, initial-scale=1.0"),
        meta(name="description", content=description),
        meta(property="og:title",       content=page_title),
        meta(property="og:description", content=description),
        meta(property="og:type",        content="website"),
        meta(property="og:url",         content=SITE_URL),
        title(page_title),
        link(rel="preconnect", href="https://fonts.googleapis.com"),
        link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=""),
        link(rel="stylesheet",
             href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=DM+Sans:wght@300;400;500&display=swap"),
        link(rel="stylesheet", href=f"/static/css/main.css?v={css_hash}"),
        script(src="https://unpkg.com/htmx.org@1.9.12", defer=True),
    )


# ── Landing Header ────────────────────────────────────────

def build_header(active: str = "home"):
    nav_links = [
        ("home",  "/",      "htmforge"),
        ("demo",  "/demo",  "Live Demo →"),
    ]
    nav_items = [
        a(label, href=href,
          class_=f"nav-link {'nav-active' if key == active else ''}")
        for key, href, label in nav_links
    ]
    return header(
        div(
            # Logo
            a(
                div(
                    span("⚒", class_="logo-mark"),
                    div(
                        span("htmforge", class_="logo-name"),
                        span(f"v{HTMFORGE_VERSION} · MIT · PyPI", class_="logo-sub"),
                        class_="logo-text-block",
                    ),
                    class_="logo-inner",
                ),
                href="/", class_="logo",
            ),
            nav(*nav_items, class_="main-nav"),
            div(
                a("pip install htmforge", href=PYPI_URL,
                  target="_blank", rel="noopener",
                  class_="install-badge"),
                class_="header-right",
            ),
            class_="header-inner",
        ),
        class_="site-header",
    )


# ── Demo Header ───────────────────────────────────────────

def build_demo_header(active: str = "dashboard"):
    nav_links = [
        ("dashboard", "/demo",         "Dashboard"),
        ("users",     "/demo/users",   "Users"),
    ]
    nav_items = [
        a(label, href=href,
          class_=f"demo-nav-link {'demo-nav-active' if key == active else ''}")
        for key, href, label in nav_links
    ]
    return header(
        div(
            a(
                div(
                    span("⚒", class_="logo-mark"),
                    div(
                        span("htmforge", class_="logo-name"),
                        span("Admin Demo", class_="logo-sub"),
                        class_="logo-text-block",
                    ),
                    class_="logo-inner",
                ),
                href="/", class_="logo",
            ),
            nav(*nav_items, class_="demo-nav"),
            a("← Zurück zur Doku", href="/", class_="back-to-docs"),
            class_="header-inner",
        ),
        class_="site-header demo-header",
    )


# ── Footer ────────────────────────────────────────────────

def build_footer():
    return footer(
        div(
            span("htmforge · ", class_="dim"),
            a(f"v{HTMFORGE_VERSION}", href=PYPI_URL, target="_blank",
              rel="noopener", class_="accent-link"),
            span(" · MIT License", class_="dim"),
            class_="footer-left",
        ),
        div(
            a("Impressum", href="/impressum", class_="footer-link"),
            span(" · ", class_="dim"),
            a("Datenschutz", href="/datenschutz", class_="footer-link"),
            class_="footer-center",
        ),
        div(
            a("PyPI ↗",    href=PYPI_URL,    target="_blank", rel="noopener", class_="footer-link"),
            span(" · ", class_="dim"),
            a("GitHub ↗",  href=GITHUB_URL,  target="_blank", rel="noopener", class_="footer-link"),
            span(" · ", class_="dim"),
            a("nepidesk.de ↗", href="https://nepidesk.de", class_="footer-link"),
            class_="footer-right",
        ),
        class_="site-footer",
    )


# ── Page shell ────────────────────────────────────────────

def _page(page_title: str, description: str, hdr, content, css_hash="", js_hash=""):
    page = html(
        _head(page_title, description, css_hash),
        body(
            hdr,
            main(*content, class_="demo-page" if "demo" in page_title.lower() else "page-main"),
            build_footer(),
            script(src=f"/static/js/main.js?v={js_hash}", defer=True),
        ),
        lang="de",
    )
    return "<!DOCTYPE html>\n" + render(page)


# ══════════════════════════════════════════════════════════
#  LANDING PAGE
# ══════════════════════════════════════════════════════════

def build_hero():
    return section(
        div(class_="parallax-grid", data_speed="0.3"),
        div(class_="parallax-glow parallax-glow-1", data_speed="0.5"),
        div(class_="parallax-glow parallax-glow-2", data_speed="0.2"),
        div(
            div(
                span("", class_="eyebrow-dot"),
                span(f"pip install htmforge=={HTMFORGE_VERSION}", class_="eyebrow-code"),
                class_="eyebrow",
            ),
            h1(
                span("htm", class_="hero-word-dim"),
                span("forge", class_="hero-word-accent"),
                class_="hero-logotype",
            ),
            p(HERO_CLAIM, class_="hero-claim"),
            p(HERO_SUB,   class_="hero-sub"),
            div(
                a("Live Demo →",    href="/demo",   class_="cta-primary"),
                a("PyPI ↗",         href=PYPI_URL,  target="_blank", rel="noopener", class_="cta-secondary"),
                a("GitHub ↗",       href=GITHUB_URL, target="_blank", rel="noopener", class_="cta-secondary"),
                class_="hero-ctas",
            ),
            # Install-Zeile
            div(
                span("$", class_="prompt"),
                span(INSTALL_CMD, class_="install-cmd"),
                class_="install-line",
            ),
            div(class_="hud-corner hud-tl"),
            div(class_="hud-corner hud-tr"),
            div(class_="hud-corner hud-bl"),
            div(class_="hud-corner hud-br"),
            class_="hero-box",
        ),
        class_="hero-section", id="hero",
    )


def build_concepts():
    cards = [
        div(
            div(span(c["num"], class_="concept-num"), class_="concept-meta"),
            h3(c["title"], class_="concept-title"),
            p(c["desc"],   class_="concept-desc"),
            class_="concept-card reveal",
            data_delay=str(i * 100),
        )
        for i, c in enumerate(CONCEPTS)
    ]
    return section(
        _section_head("01", "Das Konzept"),
        div(*cards, class_="concepts-grid"),
        class_="section-block", id="konzept",
    )


def build_code_examples():
    def example(ex: dict, i: int):
        return div(
            div(
                h3(ex["title"], class_="example-title"),
                p(ex["desc"],   class_="example-desc"),
                class_="example-head",
            ),
            div(
                div(
                    div(
                        span("python", class_="code-lang"),
                        class_="code-bar",
                    ),
                    div(raw(f"<pre><code>{_escape(ex['code'])}</code></pre>"), class_="code-body"),
                    class_="code-panel",
                ),
                div(
                    div(
                        span("output", class_="code-lang code-lang-out"),
                        class_="code-bar code-bar-out",
                    ),
                    div(
                        div(raw(ex["output"]), class_="output-rendered"),
                        div(
                            span("HTML:", class_="output-label"),
                            raw(f"<pre><code>{_escape(ex['output'])}</code></pre>"),
                            class_="output-source",
                        ),
                        class_="output-body",
                    ),
                    class_="code-panel output-panel",
                ),
                class_="example-split",
            ),
            class_="code-example reveal",
            data_delay=str(i * 80),
        )

    examples = [example(ex, i) for i, ex in enumerate(CODE_EXAMPLES)]
    return section(
        _section_head("02", "Wie es funktioniert",
                      "Python-Code links, HTML-Output rechts — was du schreibst ist was du kriegst."),
        div(*examples, class_="examples-list"),
        class_="section-block", id="beispiele",
    )


def build_demo_teaser():
    d = DEMO_INTRO
    return section(
        div(
            div(
                span("LIVE DEMO", class_="teaser-eyebrow"),
                h2(d["title"], class_="teaser-title"),
                p(d["desc"],   class_="teaser-desc"),
                a(d["cta"],    href=d["url"], class_="cta-primary"),
                class_="teaser-content",
            ),
            div(
                # Mini-Vorschau der Admin UI
                div(
                    div(
                        span("● ", class_="win-dot win-red"),
                        span("● ", class_="win-dot win-amber"),
                        span("●",  class_="win-dot win-green"),
                        span(" htmforge admin demo", class_="win-title"),
                        class_="win-bar",
                    ),
                    div(
                        _mini_stat("Users",   "7",  "green"),
                        _mini_stat("Active",  "5",  "neon"),
                        _mini_stat("Admins",  "1",  "amber"),
                        _mini_stat("API Keys","7",  "neon"),
                        class_="mini-stats",
                    ),
                    div(
                        _mini_row("Ada Lovelace",   "admin",   "active"),
                        _mini_row("Grace Hopper",   "editor",  "active"),
                        _mini_row("Alan Turing",    "editor",  "active"),
                        _mini_row("Linus Torvalds", "viewer",  "active"),
                        class_="mini-table",
                    ),
                    class_="mini-browser",
                ),
                class_="teaser-preview",
            ),
            class_="teaser-split",
        ),
        class_="section-block teaser-section", id="demo",
    )


def _mini_stat(label, value, color):
    return div(
        span(value, class_=f"mini-stat-val color-{color}"),
        span(label, class_="mini-stat-label"),
        class_="mini-stat",
    )


def _mini_row(name, role, status):
    return div(
        span(name,   class_="mini-cell mini-name"),
        span(role,   class_=f"mini-cell mini-role role-{role}"),
        span(status, class_=f"mini-cell mini-status status-{status}"),
        class_="mini-row",
    )


def build_landing(css_hash="", js_hash=""):
    return _page(
        "htmforge — HTML in Python ohne Templates",
        "Open-Source Python-Bibliothek für typsicheres HTML-Rendering. Kein Jinja, kein Template-Ordner.",
        build_header("home"),
        [build_hero(), build_concepts(), build_code_examples(), build_demo_teaser()],
        css_hash, js_hash,
    )


# ══════════════════════════════════════════════════════════
#  ADMIN DEMO — shared atoms
# ══════════════════════════════════════════════════════════

def _role_badge(role: str):
    return span(role, class_=f"badge badge-role role-{role}")


def _status_badge(status: str):
    pip = span("", class_=f"pip {'pip-online' if status == 'active' else 'pip-offline'}")
    return span(pip, status, class_=f"badge badge-status status-{status}")


def _stat_card(label: str, value, color: str = "neon", index: int = 0):
    return div(
        span(str(value), class_=f"stat-value color-{color}"),
        span(label,      class_="stat-label"),
        class_="stat-card reveal",
        data_delay=str(index * 80),
    )


def _flash(message: str, kind: str = "success"):
    """Inline-Flash-Nachricht (kein JS nötig)."""
    return div(
        span("✓ " if kind == "success" else "✗ ", class_="flash-icon"),
        span(message, class_="flash-text"),
        class_=f"flash flash-{kind}",
    ) if message else span("")


def _form_field(lbl: str, name: str, value: str = "", type_: str = "text",
                required: bool = True, placeholder: str = ""):
    return div(
        label(lbl, for_=name, class_="field-label"),
        input(
            type=type_, name=name, id=name,
            value=value, placeholder=placeholder,
            class_="field-input",
            **({"required": True} if required else {}),
        ),
        class_="form-field",
    )


def _select_field(lbl: str, name: str, options: list[tuple], current: str = ""):
    opts = [
        option(label, value=val, **({"selected": True} if val == current else {}))
        for val, label in options
    ]
    return div(
        label(lbl, for_=name, class_="field-label"),
        select(*opts, name=name, id=name, class_="field-select"),
        class_="form-field",
    )


# ── Dashboard ─────────────────────────────────────────────

def build_dashboard(stats: dict, css_hash="", js_hash=""):
    stat_cards = [
        _stat_card("Gesamt",   stats["total_users"],    "neon",  0),
        _stat_card("Aktiv",    stats["active_users"],   "green", 1),
        _stat_card("Inaktiv",  stats["inactive_users"], "amber", 2),
        _stat_card("Admins",   stats["admins"],         "neon",  3),
        _stat_card("API Keys", stats["api_keys"],       "neon",  4),
    ]

    # Code-Snippet das diese Seite erzeugt hat
    snippet = """\
# So wird diese Dashboard-Seite gerendert:

def build_dashboard(stats: dict):
    cards = [
        stat_card("Gesamt",  stats["total_users"],  "neon"),
        stat_card("Aktiv",   stats["active_users"], "green"),
        # ...
    ]
    return _page(
        "Dashboard",
        build_demo_header("dashboard"),
        [section(*cards, class_="stats-grid"), ...],
    )

# stat_card ist eine einfache Python-Funktion:
def stat_card(label, value, color):
    return div(
        span(str(value), class_=f"stat-value color-{color}"),
        span(label,      class_="stat-label"),
        class_="stat-card",
    )"""

    content = [
        section(
            div(
                h1("Dashboard", class_="demo-page-title"),
                a("+ Neuer User", href="/demo/users/new", class_="btn-primary"),
                class_="demo-page-head",
            ),
            div(*stat_cards, class_="stats-grid"),
            class_="demo-section-main",
        ),
        _code_aside(snippet, "Das Dashboard — 5 Stat-Cards, alle aus Python-Funktionen."),
    ]
    return _page(
        "Dashboard — htmforge Admin Demo",
        "htmforge Admin Demo: Dashboard",
        build_demo_header("dashboard"),
        content, css_hash, js_hash,
    )


# ── User-Tabelle ──────────────────────────────────────────

def build_user_table(users, flash_msg: str = "", flash_kind: str = "success",
                     search: str = "", css_hash="", js_hash=""):
    rows = [
        tr(
            td(str(u["id"]),           class_="td"),
            td(u["name"],              class_="td td-name"),
            td(u["email"],             class_="td td-mono"),
            td(_role_badge(u["role"]), class_="td"),
            td(_status_badge(u["status"]), class_="td"),
            td(u["created_at"][:10],   class_="td td-mono td-dim"),
            td(
                a("Edit", href=f"/demo/users/{u['id']}/edit", class_="tbl-btn"),
                form(
                    input(type="hidden", name="_method", value="DELETE"),
                    button("Delete", type="submit", class_="tbl-btn tbl-btn-danger",
                           onclick="return confirm('User " + u["name"] + " wirklich löschen?')"),
                    action=f"/demo/users/{u['id']}/delete", method="POST",
                ),
                class_="td td-actions",
            ),
            class_="tbl-row",
        )
        for u in users
    ]

    snippet = """\
# Jede Tabellenzeile ist eine Python-Funktion:
def user_row(user):
    return tr(
        td(user["name"],              class_="td"),
        td(_role_badge(user["role"]), class_="td"),
        td(_status_badge(user["status"]), class_="td"),
        td(
            a("Edit", href=f"/users/{user['id']}/edit",
              class_="tbl-btn"),
            class_="td td-actions",
        ),
        class_="tbl-row",
    )

# Tabelle = Liste von Zeilen:
rows = [user_row(u) for u in users]
return table(thead(...), tbody(*rows))"""

    content = [
        section(
            _flash(flash_msg, flash_kind),
            div(
                h1("Users", class_="demo-page-title"),
                a("+ Neuer User", href="/demo/users/new", class_="btn-primary"),
                class_="demo-page-head",
            ),
            # Suchfeld
            form(
                input(
                    type="search", name="q", value=search,
                    placeholder="Name oder E-Mail suchen...",
                    class_="search-input",
                ),
                button("Suchen", type="submit", class_="btn-secondary"),
                action="/demo/users", method="GET",
                class_="search-form",
            ),
            div(
                table(
                    thead(
                        tr(
                            *[th(h, class_="th") for h in
                              ["ID", "Name", "E-Mail", "Rolle", "Status", "Erstellt", ""]],
                        )
                    ),
                    tbody(*rows),
                    class_="data-table",
                ),
                class_="table-wrapper",
            ),
            class_="demo-section",
        ),
        _code_aside(snippet, "Tabelle aus Python — jede Zeile eine Funktion, kein Template."),
    ]
    return _page(
        "Users — htmforge Admin Demo",
        "htmforge Admin Demo: User-Tabelle",
        build_demo_header("users"),
        content, css_hash, js_hash,
    )


# ── User-Formular ─────────────────────────────────────────

def build_user_form(user=None, error: str = "", css_hash="", js_hash=""):
    is_edit = user is not None
    title_  = f"User bearbeiten — {user['name']}" if is_edit else "Neuer User"
    action  = f"/demo/users/{user['id']}/edit" if is_edit else "/demo/users/new"

    role_opts   = [("admin","Admin"), ("editor","Editor"), ("viewer","Viewer")]
    status_opts = [("active","Aktiv"), ("inactive","Inaktiv")]

    snippet = """\
# Formular komplett in Python — kein HTML-File:
def user_form(user=None):
    is_edit = user is not None
    return form(
        _form_field("Name",  "name",
                    value=user["name"] if user else ""),
        _form_field("E-Mail","email",
                    value=user["email"] if user else "",
                    type_="email"),
        _select_field("Rolle", "role",
                      [("admin","Admin"),
                       ("editor","Editor"),
                       ("viewer","Viewer")],
                      current=user["role"] if user else ""),
        button("Speichern", type="submit",
               class_="btn-primary"),
        action=action, method="POST",
        class_="admin-form",
    )"""

    content = [
        section(
            div(
                a("← Zurück", href="/demo/users", class_="back-link"),
                class_="demo-back",
            ),
            h1(title_, class_="demo-page-title"),
            _flash(error, "error") if error else span(""),
            form(
                _form_field("Name",    "name",  value=user["name"]  if user else "",
                            placeholder="Ada Lovelace"),
                _form_field("E-Mail",  "email", value=user["email"] if user else "",
                            type_="email", placeholder="ada@example.com"),
                _select_field("Rolle",   "role",   role_opts,   current=user["role"]   if user else "viewer"),
                _select_field("Status",  "status", status_opts, current=user["status"] if user else "active"),
                div(
                    button("Speichern", type="submit", class_="btn-primary"),
                    a("Abbrechen", href="/demo/users", class_="btn-ghost"),
                    class_="form-actions",
                ),
                action=action, method="POST",
                class_="admin-form",
            ),
            class_="demo-section demo-section-narrow",
        ),
        _code_aside(snippet, "Formular aus Python — Fields sind Funktionen, kein Markup."),
    ]
    return _page(
        f"{title_} — htmforge Admin Demo",
        "htmforge Admin Demo: User-Formular",
        build_demo_header("users"),
        content, css_hash, js_hash,
    )


# ── Code-Aside ────────────────────────────────────────────

def _code_aside(snippet: str, caption: str):
    """Rechte Spalte: der Python-Code der diese Seite rendert."""
    return aside(
        div(
            span("⚒ htmforge", class_="aside-badge"),
            p(caption, class_="aside-caption"),
            div(
                div(
                    span("components.py", class_="code-lang"),
                    class_="code-bar",
                ),
                div(raw(f"<pre><code>{_escape(snippet)}</code></pre>"), class_="code-body"),
                class_="code-panel aside-code",
            ),
            class_="aside-inner",
        ),
        class_="code-aside",
    )


# ── Helpers ───────────────────────────────────────────────

def _section_head(num: str, title: str, subtitle: str = ""):
    return div(
        div(span(num, class_="section-num"), span("·", class_="section-dot"), class_="section-meta"),
        h2(
            span("", class_="typewriter-text"),
            span("▌", class_="typewriter-cursor"),
            data_typewriter=title,
            class_="section-title typewriter",
        ),
        p(subtitle, class_="section-sub") if subtitle else span(""),
        class_="section-head",
    )


def _escape(text: str) -> str:
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))


# ── Impressum ────────────────────────────────────────────

def build_impressum_page(css_hash="", js_hash=""):
    imp = IMPRESSUM

    def row(label: str, *children):
        return div(
            span(label, class_="legal-key"),
            div(*children, class_="legal-val"),
            class_="legal-row",
        )

    content = [
        section(
            div(
                a("← Zurück", href="/", class_="back-link"),
                class_="subpage-back",
            ),
            h1("Impressum", class_="legal-page-title"),
            p("Angaben gemäß § 5 TMG", class_="legal-subtitle"),

            # Verantwortlicher
            div(
                h2("Verantwortlicher", class_="legal-section-title"),
                row("Name",         span(imp["name"],       class_="legal-text")),
                row("Anschrift",    span(imp["strasse"],    class_="legal-text"),
                                    span(imp["ort"],        class_="legal-text")),
                row("Rechtsform",   span(imp["rechtsform"], class_="legal-text")),
                row("E-Mail",       a(imp["email"], href=f"mailto:{imp['email']}", class_="legal-link")),
                class_="legal-block",
            ),

            # Hinweis Steuernummer
            div(
                h2("Steuerliche Angaben", class_="legal-section-title"),
                p(
                    "Eine Umsatzsteuer-Identifikationsnummer liegt derzeit nicht vor. "
                    "Umsatzsteuerbefreiung gemäß § 19 UStG (Kleinunternehmerregelung) "
                    "wird bei Bedarf separat kommuniziert.",
                    class_="legal-prose",
                ),
                class_="legal-block",
            ),

            # Streitschlichtung
            div(
                h2("Streitschlichtung", class_="legal-section-title"),
                p(
                    "Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) bereit: ",
                    a("https://ec.europa.eu/consumers/odr",
                      href="https://ec.europa.eu/consumers/odr",
                      target="_blank", rel="noopener", class_="legal-link"),
                    span(". Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren "
                         "vor einer Verbraucherschlichtungsstelle teilzunehmen."),
                    class_="legal-prose",
                ),
                class_="legal-block",
            ),

            # Haftung
            div(
                h2("Haftung für Inhalte", class_="legal-section-title"),
                p(
                    "Als Diensteanbieter sind wir gemäß § 7 Abs. 1 TMG für eigene Inhalte auf diesen Seiten "
                    "nach den allgemeinen Gesetzen verantwortlich. Nach §§ 8 bis 10 TMG sind wir als "
                    "Diensteanbieter jedoch nicht verpflichtet, übermittelte oder gespeicherte fremde "
                    "Informationen zu überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige "
                    "Tätigkeit hinweisen.",
                    class_="legal-prose",
                ),
                class_="legal-block",
            ),

            class_="legal-page section-block",
        ),
    ]
    return _page_shell(
        "Impressum", "Impressum — NepiDesk",
        "", content, css_hash, js_hash,
    )


# ── Datenschutz ──────────────────────────────────────────

def build_datenschutz_page(css_hash="", js_hash=""):
    ds = DATENSCHUTZ

    def block(title: str, *paras):
        return div(
            h2(title, class_="legal-section-title"),
            *[p(text, class_="legal-prose") for text in paras],
            class_="legal-block",
        )

    content = [
        section(
            div(
                a("← Zurück", href="/", class_="back-link"),
                class_="subpage-back",
            ),
            h1("Datenschutzerklärung", class_="legal-page-title"),
            p("Zuletzt aktualisiert: Juni 2025", class_="legal-subtitle"),

            block(
                "1. Verantwortlicher",
                f"Verantwortlich im Sinne der DSGVO: {ds['verantwortlicher_name']}, "
                f"erreichbar unter {ds['verantwortlicher_email']}.",
            ),

            block(
                "2. Welche Daten wir erheben",
                "Diese Website erhebt keine personenbezogenen Daten durch Tracking, "
                "Cookies oder Analyse-Tools. Es werden keine Cookies gesetzt.",
                "Beim Aufruf der Website werden durch den Webserver technisch notwendige "
                "Server-Logs gespeichert (IP-Adresse, Zeitstempel, aufgerufene URL, "
                "HTTP-Statuscode, verwendeter Browser). Diese Daten dienen ausschließlich "
                "der technischen Fehlerdiagnose und werden nach spätestens 7 Tagen gelöscht.",
            ),

            block(
                "3. Hosting & Infrastruktur",
                f"Die Website wird auf einem eigenen, privat betriebenen Server in Deutschland gehostet. "
                "Es werden keine externen Hosting-Anbieter eingesetzt.",
                "Der Datenverkehr wird über Cloudflare (Cloudflare, Inc., 101 Townsend St., "
                "San Francisco, CA 94107, USA) geleitet. Cloudflare agiert dabei als "
                "Reverse-Proxy und kann dabei technische Metadaten (IP-Adresse, Request-Header) "
                "verarbeiten. Die eigentliche IP-Adresse des Servers wird dabei nicht öffentlich "
                "exponiert. Weitere Informationen: https://www.cloudflare.com/privacypolicy/",
            ),

            block(
                "4. Kontaktaufnahme per E-Mail",
                "Wenn Sie uns per E-Mail kontaktieren, werden die von Ihnen übermittelten Daten "
                "(E-Mail-Adresse, ggf. Name und Nachrichteninhalt) ausschließlich zur Bearbeitung "
                "Ihrer Anfrage verwendet. Diese Daten werden nicht an Dritte weitergegeben und "
                "nach Abschluss der Anfrage gelöscht, sofern keine gesetzlichen Aufbewahrungsfristen bestehen.",
            ),

            block(
                "5. Ihre Rechte",
                "Sie haben jederzeit das Recht auf Auskunft (Art. 15 DSGVO), Berichtigung (Art. 16 DSGVO), "
                "Löschung (Art. 17 DSGVO), Einschränkung der Verarbeitung (Art. 18 DSGVO) sowie "
                "Datenübertragbarkeit (Art. 20 DSGVO).",
                "Zur Ausübung Ihrer Rechte genügt eine E-Mail an kontakt@nepidesk.de. "
                "Sie haben zudem das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren.",
            ),

            block(
                "6. Externe Links",
                "Diese Website enthält Links zu externen Websites (z. B. PyPI, GitHub, Cloudflare). "
                "Für die Datenschutzpraktiken dieser externen Anbieter übernehmen wir keine Verantwortung.",
            ),

            block(
                "7. Aktualität",
                "Wir behalten uns vor, diese Datenschutzerklärung bei Bedarf anzupassen, "
                "etwa bei technischen Änderungen der Website oder neuen gesetzlichen Anforderungen.",
            ),

            class_="legal-page section-block",
        ),
    ]
    return _page_shell(
        "Datenschutz", "Datenschutzerklärung — NepiDesk",
        "", content, css_hash, js_hash,
    )

# ── aside fehlt im htmforge-Import ───────────────────────
# Workaround: aside als generisches Element

from htmforge.elements import div as _div

def aside(*children, **attrs):
    """aside-Element via htmforge."""
    attrs.setdefault("class_", "")
    cls = attrs.pop("class_", "")
    return _div(*children, class_=f"aside-wrapper {cls}".strip())