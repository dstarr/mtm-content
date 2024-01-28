import os
import secrets
import uuid
from flask import Flask, render_template, redirect, url_for, session, request
from flask_session import Session
import config
import msal
import identity.web

from content.views import content_bp
from playlists.views import playlists_bp
from search.views import search_bp

from content.models.list_model import ListItemModel, ListModel
from services.content_service import ContentService
from msal import PublicClientApplication


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)

app.register_blueprint(content_bp, url_prefix='/content')
app.register_blueprint(playlists_bp, url_prefix='/playlists')
app.register_blueprint(search_bp, url_prefix='/search')

msal_app = msal.ConfidentialClientApplication(
    config.AZURE_CLIENT_ID, 
    authority=config.AZURE_AUTHORITY,
    client_credential=config.AZURE_CLIENT_SECRET)

# @app.before_request
# def check_user_authenticated():
#     if not session.get('user'):
#         return redirect(url_for('login'))

@app.route('/')
def index():
    if not session.get('user'):
        return redirect(url_for('login'))
    return f"Welcome {session['user']['name']}!"

@app.route('/login')
def login():
    session['state'] = str(uuid.uuid4())
    auth_url = msal_app.get_authorization_request_url(config.AZURE_SCOPE, state=session['state'], redirect_uri=url_for('authorized', _external=True))
    return redirect(auth_url)

@app.route(config.AZURE_REDIRECT_PATH)
def authorized():
    if request.args.get('state') != session.get("state"):
        return redirect(url_for('index'))  # No-Auth if state does not match
    
    result = msal_app.acquire_token_by_authorization_code(
        request.args['code'],
        scopes=config.AZURE_SCOPE,  # Misspelled scope would cause an HTTP 400 error here
        redirect_uri=url_for('content.index', _external=True),
        )

    if 'error' in result:
        return f"Login failure: {result.get('error_description')}"

    session['user'] = result.get('id_token_claims')
    
    return redirect(url_for('index'))

# @app.context_processor
# def inject_user():
#     return dict(user=session['user'])

if __name__ == '__main__':
    app.run(port=config.FLASK_PORT, debug=config.FLASK_DEBUG)