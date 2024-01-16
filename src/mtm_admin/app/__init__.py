from flask import Flask
from .playlists import playlists

app = Flask(__name__)
app.register_blueprint(playlists, url_prefix='/playlists')