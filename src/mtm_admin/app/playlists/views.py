from flask import Blueprint, render_template
from content_service import ContentService

content_service = ContentService()

from . import playlists

@playlists.route('/playlists')
def playlists():
    playlists = ContentService.get_playlists()
    
    return render_template('index.html', model=playlists["playlists"])
    