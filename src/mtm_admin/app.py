import os
import sys
from flask import Flask, render_template, request
import config

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'services'))
sys.path.append(os.path.join(current_dir, 'playlists'))
sys.path.append(os.path.join(current_dir, 'modules/models'))

from playlists.views import playlists_bp
from content.views import content_bp
from search.views import search_bp
from content.models.list_model import ListItemModel, ListModel
from services.content_service import ContentService


app = Flask(__name__)

app.register_blueprint(playlists_bp, url_prefix='/playlists')
app.register_blueprint(content_bp, url_prefix='/content')
app.register_blueprint(search_bp, url_prefix='/search')

@app.route('/')
def home():
    content_service = ContentService()
    
    content = content_service.get_all_content()
    
    return render_template('index.html', model=content)

if __name__ == '__main__':
    if config.FLASK_DEBUG == '1':
        print('Running in debug mode')
        print(app.url_map)
        app.run(debug=True, port=config.FLASK_PORT, use_reloader=True)
    else:
        print('Running in production mode')
        app.run(port=config.FLASK_PORT, use_reloader=False)