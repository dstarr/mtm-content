import os
import secrets
import sys
from flask import Flask, render_template, redirect, url_for, session, request
import config

from content.views import content_bp
from playlists.views import playlists_bp
from search.views import search_bp

from content.models.list_model import ListItemModel, ListModel
from services.content_service import ContentService


app = Flask(__name__)

app.register_blueprint(content_bp, url_prefix='/content')
app.register_blueprint(playlists_bp, url_prefix='/playlists')
app.register_blueprint(search_bp, url_prefix='/search')


app.config.update({
    "SECRET_KEY": secrets.token_urlsafe(16),  # Flask session secret key
    "CLIENT_ID": config.AZURE_CLIENT_ID,
    "CLIENT_SECRET": config.AZURE_CLIENT_SECRET,
    "AUTHORITY": f"https://login.microsoftonline.com/{config.AZURE_TENANT_ID}",
    "REDIRECT_PATH": "/getAToken",
    "SCOPE": ["User.Read"],  # Add other scopes/permissions as needed
})

@app.route('/')
def home():
    return redirect(url_for('content.index'))

if __name__ == '__main__':
    app.run(port=config.FLASK_PORT, debug=config.FLASK_DEBUG)