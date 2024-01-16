import os
import sys
from flask import Flask, redirect, render_template, request, url_for
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'services'))
sys.path.append(os.path.join(current_dir, 'models/modules'))


from list_model import ListItemModel, ListModel
from content_service import ContentService

content_service = ContentService()

load_dotenv()

app = Flask(__name__)

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

@app.route('/modules/<module_id>')
def module_detail(module_id):
    module = content_service.get_module(module_id)
    
    from detail_model import DetailModel
    model = DetailModel(playlist=module["playlist"], content=module["module"])
    
    return render_template('modules/detail.html', model=model)

@app.route('/modules/<module_id>/edit')
def module_edit(module_id):
    module = content_service.get_module(module_id)["module"]
    playlists = content_service.get_playlists()
    
    from edit_model import EditModel
    model = EditModel(playlists=playlists, content=module)
    
    return render_template('modules/edit.html', model=model)

@app.route('/modules/update', methods=['POST'])
def module_update():
    print(request.form)
    
    content_service.update_module(new_values=request.form)
    return redirect(url_for('module_detail', module_id=request.form["id"]))

@app.route('/tags')
def tags():
    pass

# @app.route('/tags/<int:tag_id>')

# @app.route('/tags/<int:tag_id>/delete')

# @app.route('/playlists')

# @app.route('/playlists/<int:playlist_id>')

# @app.route('/playlists/<int:playlist_id>')

if __name__ == '__main__':
    app.run(debug=True, port=3000)
