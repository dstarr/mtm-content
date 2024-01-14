import os
import sys
from flask import Flask, render_template
from dotenv import load_dotenv

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(current_dir, 'services'))

from content_service import ComtentService

content_service = ComtentService()

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    modules = content_service.get_all_modules()
    return render_template('index.html', modules=modules)

@app.route('/modules/<module_id>')
def module_detail(module_id):
    module = content_service.get_module(module_id)
    return render_template('modules/detail.html', module=module)

@app.route('/tags')
def tags():
    tags = content_service.get_all_tags()
    return render_template('tags.html', tags=tags)

# @app.route('/modules/<int:module_id>/edit')
# 
# @app.route('/tags/<int:tag_id>')
# @app.route('/tags/<int:tag_id>/delete')
# @app.route('/playlists')
# @app.route('/playlists/<int:playlist_id>')
# @app.route('/playlists/<int:playlist_id>')




if __name__ == '__main__':
    app.run(debug=True, port=3000)
