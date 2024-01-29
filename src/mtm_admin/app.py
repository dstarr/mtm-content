import os
from flask import Flask, render_template, redirect, url_for, session, request
import config
import msal
from werkzeug.middleware.proxy_fix import ProxyFix

from content.views import content_bp
from playlists.views import playlists_bp
from search.views import search_bp

from content.models.list_model import ListItemModel, ListModel
from services.content_service import ContentService

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.config['SECRET_KEY'] = os.urandom(16)

app.register_blueprint(content_bp, url_prefix='/content')
app.register_blueprint(playlists_bp, url_prefix='/playlists')
app.register_blueprint(search_bp, url_prefix='/search')

# set up session
app.secret_key = os.urandom(16)

# MSAL configuration
AUTHORITY = config.AZURE_AUTHORITY
app.config["MSAL_AUTHORIZE_ENDPOINT"] = f"{AUTHORITY}/oauth2/v2.0/authorize"
app.config["MSAL_CLIENT_ID"] = config.AZURE_CLIENT_ID
app.config["MSAL_CLIENT_SECRET"] = config.AZURE_CLIENT_SECRET
app.config["MSAL_SCOPE"] = ["User.Read"]
app.config["MSAL_TOKEN_ENDPOINT"] = f"{AUTHORITY}/oauth2/v2.0/token"

# MSAL instance
msal_app = msal.ConfidentialClientApplication(
    app.config["MSAL_CLIENT_ID"],
    authority=AUTHORITY,
    client_credential=app.config["MSAL_CLIENT_SECRET"]
)

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("content.index"))
    else:
        return redirect(url_for("login"))

@app.route("/login")
def login():
    auth_url = msal_app.get_authorization_request_url(
        app.config["MSAL_SCOPE"],
        redirect_uri=url_for("authorized", _external=True)
    )
    return redirect(auth_url)

@app.route("/authorized")
def authorized():
    result = msal_app.acquire_token_by_authorization_code(
        request.args["code"],
        scopes=app.config["MSAL_SCOPE"],
        redirect_uri=url_for("authorized", _external=True)
    )
    if "error" in result:
        return f"Error: {result['error_description']}"

    session["user"] = result.get("id_token_claims")
    
    print(session["user"])
    
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.clear()
    return render_template("auth_signed_out.html")

# @app.before_request
# def check_user_authenticated():
#     if "user" not in session:
#         return redirect(url_for('login'))

@app.context_processor
def inject_user():
    if "user" in session:
        return dict(user=session['user'])
    else:
        return dict(user=None)

if __name__ == '__main__':
    app.run(port=config.FLASK_PORT, debug=config.FLASK_DEBUG)