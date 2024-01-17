from flask import Blueprint, render_template
from content_service import ContentService

playlists_bp = Blueprint(
    "playlists", __name__, template_folder="templates", static_folder="static"
)

content_service = ContentService()

@playlists_bp.route("/")
def playlists_index():
    playlists = content_service.get_playlists()

    return render_template("playlists_index.html", model=playlists)


@playlists_bp.route("/detail/<playlist_id>")
def playlists_detail(playlist_id):
    playlist = content_service.get_playlist(id=playlist_id)
    
    return render_template("playlists_detail.html", model=playlist)

