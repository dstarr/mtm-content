from flask import Blueprint, redirect, render_template, request, url_for
from playlists.model.playlist_detail_model import PlaylistDetailModel
from services.content_service import ContentService

playlists_bp = Blueprint(
    "playlists", __name__, 
    template_folder="templates", 
    static_folder="static"
)

content_service = ContentService()

@playlists_bp.route("/")
def playlists_index():
    playlists = content_service.get_playlists()
    return render_template("playlists_index.html", model=playlists)

@playlists_bp.route("/<playlist_id>")
def playlist_detail(playlist_id):
    playlist = content_service.get_playlist(id=playlist_id)
    contents = []
    
    for content_id in playlist["content"]:
        content = content_service.get_content(content_id=content_id)
        contents.append(
            { "id": content["id"], "title": content["title"] }
        )
        
    model = PlaylistDetailModel(content=contents, playlist=playlist)

    return render_template("playlists_detail.html", model=model)

@playlists_bp.route("edit/<playlist_id>", methods=["GET", "POST"])
def playlist_edit(playlist_id):
    if request.method == "POST":

        content_service.update_playlist_name(
            id=playlist_id,
            name=request.form["name"],
        )
        
        return redirect(url_for('playlists.playlists_detail', playlist_id=playlist_id))
    
    elif request.method == "GET":
        playlist = content_service.get_playlist(id=playlist_id)

        return render_template("playlists_edit.html", model=playlist)

