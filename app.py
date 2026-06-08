"""
htmforge-demo — app.py
Flask App. Nur Routes.
"""

import hashlib
from flask import Flask, Response, request, redirect, url_for

from components import (
    build_landing,
    build_dashboard,
    build_user_table,
    build_user_form,
    build_order_table,
    build_order_form,
    build_impressum_page,
    build_datenschutz_page,
)
from db import (
    init_db,
    get_users, get_user, create_user, update_user, delete_user, get_stats,
    get_orders, get_order, create_order, update_order_status, delete_order, get_order_stats,
)

app = Flask(__name__, static_folder="static")


def _h(path: str) -> str:
    try:
        return hashlib.md5(open(path, "rb").read()).hexdigest()[:8]
    except FileNotFoundError:
        return "0"


def _hashes():
    return _h("static/css/main.css"), _h("static/js/main.js")


# ── Init ──────────────────────────────────────────────────

with app.app_context():
    init_db()


# ── Landing ───────────────────────────────────────────────

@app.route("/")
def index():
    css, js = _hashes()
    return Response(build_landing(css, js), mimetype="text/html")


# ── Legal ──────────────────────────────────────────────── 

@app.route("/impressum")
def impressum():
    css, js = _hashes()
    return Response(build_impressum_page(css, js), mimetype="text/html")


@app.route("/datenschutz")
def datenschutz():
    css, js = _hashes()
    return Response(build_datenschutz_page(css, js), mimetype="text/html")


# ── Demo: Dashboard ───────────────────────────────────────

@app.route("/demo")
def demo_dashboard():
    css, js = _hashes()
    return Response(
        build_dashboard(get_stats(), get_order_stats(), css, js), 
        mimetype="text/html"
    )


# ── Demo: Users ───────────────────────────────────────────

@app.route("/demo/users")
def demo_users():
    css, js = _hashes()
    search = request.args.get("q", "")
    flash  = request.args.get("flash", "")
    kind   = request.args.get("kind", "success")
    users  = get_users(search)
    return Response(build_user_table(users, flash, kind, search, css, js), mimetype="text/html")


@app.route("/demo/users/new", methods=["GET", "POST"])
def demo_user_new():
    css, js = _hashes()
    if request.method == "POST":
        name   = request.form.get("name",   "").strip()
        email  = request.form.get("email",  "").strip()
        role   = request.form.get("role",   "viewer")
        status = request.form.get("status", "active")
        if not name or not email:
            return Response(
                build_user_form(error="Name und E-Mail sind Pflichtfelder.", css_hash=css, js_hash=js),
                mimetype="text/html",
            )
        try:
            create_user(name, email, role, status)
        except Exception:
            return Response(
                build_user_form(error="E-Mail bereits vergeben.", css_hash=css, js_hash=js),
                mimetype="text/html",
            )
        return redirect(url_for("demo_users", flash="User erfolgreich erstellt.", kind="success"))
    return Response(build_user_form(css_hash=css, js_hash=js), mimetype="text/html")


@app.route("/demo/users/<int:user_id>/edit", methods=["GET", "POST"])
def demo_user_edit(user_id: int):
    css, js = _hashes()
    user = get_user(user_id)
    if not user:
        return redirect(url_for("demo_users", flash="User nicht gefunden.", kind="error"))
    if request.method == "POST":
        name   = request.form.get("name",   "").strip()
        email  = request.form.get("email",  "").strip()
        role   = request.form.get("role",   user["role"])
        status = request.form.get("status", user["status"])
        if not name or not email:
            return Response(
                build_user_form(dict(user), error="Name und E-Mail sind Pflichtfelder.", css_hash=css, js_hash=js),
                mimetype="text/html",
            )
        try:
            update_user(user_id, name, email, role, status)
        except Exception:
            return Response(
                build_user_form(dict(user), error="E-Mail bereits vergeben.", css_hash=css, js_hash=js),
                mimetype="text/html",
            )
        return redirect(url_for("demo_users", flash=f"{name} erfolgreich aktualisiert.", kind="success"))
    return Response(build_user_form(dict(user), css_hash=css, js_hash=js), mimetype="text/html")


@app.route("/demo/users/<int:user_id>/delete", methods=["POST"])
def demo_user_delete(user_id: int):
    user = get_user(user_id)
    if user:
        delete_user(user_id)
        return redirect(url_for("demo_users", flash=f"{user['name']} gelöscht.", kind="success"))
    return redirect(url_for("demo_users", flash="User nicht gefunden.", kind="error"))


# ── Demo: Orders ──────────────────────────────────────────

@app.route("/demo/orders")
def demo_orders():
    css, js = _hashes()
    search = request.args.get("q", "")
    status = request.args.get("status", "")
    flash  = request.args.get("flash", "")
    kind   = request.args.get("kind", "success")
    orders = get_orders(search, status)
    stats  = get_order_stats()
    return Response(
        build_order_table(orders, stats, flash, kind, search, status, css, js),
        mimetype="text/html",
    )


@app.route("/demo/orders/new", methods=["GET", "POST"])
def demo_order_new():
    css, js = _hashes()
    if request.method == "POST":
        order_nr = request.form.get("order_nr", "").strip()
        customer = request.form.get("customer", "").strip()
        product  = request.form.get("product",  "").strip()
        status   = request.form.get("status",   "offen")
        try:
            amount = float(request.form.get("amount", "0").replace(",", "."))
        except ValueError:
            amount = 0.0
        if not order_nr or not customer or not product:
            return Response(
                build_order_form(error="Order-Nr, Kunde und Produkt sind Pflichtfelder.", css_hash=css, js_hash=js),
                mimetype="text/html",
            )
        try:
            create_order(order_nr, customer, product, amount, status)
        except Exception:
            return Response(
                build_order_form(error="Order-Nr bereits vergeben.", css_hash=css, js_hash=js),
                mimetype="text/html",
            )
        return redirect(url_for("demo_orders", flash=f"Order {order_nr} erstellt.", kind="success"))
    return Response(build_order_form(css_hash=css, js_hash=js), mimetype="text/html")


@app.route("/demo/orders/<int:order_id>/status", methods=["POST"])
def demo_order_status(order_id: int):
    order  = get_order(order_id)
    status = request.form.get("status", "")
    if order and status:
        update_order_status(order_id, status)
        return redirect(url_for(
            "demo_orders",
            flash=f"Order {order['order_nr']} → {status}.",
            kind="success",
        ))
    return redirect(url_for("demo_orders", flash="Fehler beim Update.", kind="error"))


@app.route("/demo/orders/<int:order_id>/delete", methods=["POST"])
def demo_order_delete(order_id: int):
    order = get_order(order_id)
    if order:
        delete_order(order_id)
        return redirect(url_for(
            "demo_orders",
            flash=f"Order {order['order_nr']} gelöscht.",
            kind="success",
        ))
    return redirect(url_for("demo_orders", flash="Order nicht gefunden.", kind="error"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5101, debug=True)