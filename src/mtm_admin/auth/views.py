from flask import Blueprint, redirect, render_template, request, session, url_for
import msal

import config
import app

auth_bp = Blueprint(
    "content", __name__, 
    template_folder="templates",
    static_folder="static",
)

@auth_bp.route("/")
def index():
    if not session.get("user"):
        return redirect(url_for("login"))
    return f"Welcome {session['user']['name']}!"