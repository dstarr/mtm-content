from flask import Blueprint, render_template
from content_service import ContentService

playlists_bp = Blueprint(
    "playlists", 
    __name__, 
    template_folder="templates", 
    static_folder="static"
)

content_service = ContentService()

@playlists_bp.route('/')
def playlists_index():
    playlists = content_service.get_playlists()
    
    return render_template('playlists_index.html', model=playlists)