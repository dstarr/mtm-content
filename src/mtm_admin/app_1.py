import os
from flask import Flask, redirect, url_for, session, request
import msal
import config

app = Flask(__name__)
app.secret_key = os.urandom(16)

# Azure AD configuration
CLIENT_ID = config.AZURE_CLIENT_ID

AUTHORITY = f"https://login.microsoftonline.com/{config.AZURE_TENANT_ID}"

# MSAL configuration
app.config["MSAL_CLIENT_ID"] = config.AZURE_CLIENT_ID
app.config["MSAL_CLIENT_SECRET"] = config.AZURE_CLIENT_SECRET
app.config["MSAL_AUTHORIZE_ENDPOINT"] = f"{AUTHORITY}/oauth2/v2.0/authorize"
app.config["MSAL_TOKEN_ENDPOINT"] = f"{AUTHORITY}/oauth2/v2.0/token"
app.config["MSAL_SCOPE"] = ["User.Read"]

# MSAL instance
msal_app = msal.ConfidentialClientApplication(
    app.config["MSAL_CLIENT_ID"],
    authority=AUTHORITY,
    client_credential=app.config["MSAL_CLIENT_SECRET"]
)

@app.route("/")
def home():
    if "user" in session:
        # return f"Hello, {session['user']['displayName']}!"
        return f"Hello, {session['user']['name']}!"
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
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(port=3000)
