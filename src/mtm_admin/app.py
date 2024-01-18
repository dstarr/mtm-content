import os
import sys
from flask import Flask, redirect, render_template, request, url_for
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'services'))
sys.path.append(os.path.join(current_dir, 'playlists'))
sys.path.append(os.path.join(current_dir, 'modules/models'))

from playlists.views import playlists_bp
from modules.views import modules_bp
from modules.models.list_model import ListItemModel, ListModel
from services.content_service import ContentService

content_service = ContentService()

load_dotenv()

app = Flask(__name__)
app.register_blueprint(playlists_bp, url_prefix='/playlists')
app.register_blueprint(modules_bp, url_prefix='/modules')

print(app.url_map)

@app.route('/')
def home():
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
    app.run(debug=True, port=3000)
