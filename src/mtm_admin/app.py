import os
import sys
from flask import Flask, render_template, request
import config

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'services'))
sys.path.append(os.path.join(current_dir, 'playlists'))
sys.path.append(os.path.join(current_dir, 'modules/models'))

from playlists.views import playlists_bp
from modules.views import modules_bp
from search.views import search_bp
from modules.models.list_model import ListItemModel, ListModel
from services.content_service import ContentService


app = Flask(__name__)

app.register_blueprint(playlists_bp, url_prefix='/playlists')
app.register_blueprint(modules_bp, url_prefix='/modules')
app.register_blueprint(search_bp, url_prefix='/search')

@app.route('/')
def home():
    content_service = ContentService()
    
    modules = content_service.get_all_modules()
    playlists = content_service.get_playlists()
    
    list_model = ListModel([])
    
    for module in modules:
        
        playlist = next((p for p in playlists if p["id"] == module["playlist_id"]), None)
        
        list_item_model = ListItemModel(module=module, playlist=playlist)
        list_item_model.module = module
        
        list_model.items.append(list_item_model)
    
    return render_template('index.html', model=list_model)

if __name__ == '__main__':
    if config.FLASK_DEBUG == '1':
        print('Running in debug mode')
        print(app.url_map)
        app.run(debug=True)

    else:
        print('Running in production mode')
        app.run()