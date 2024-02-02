class PlaylistEditModel():
    
    def __init__(self, playlist, content_info_items):
        self._playlist = playlist
        self._content_info_items = content_info_items
        
    @property
    def playlist(self):
        return self._playlist
    
    @property
    def content_info_items(self):
        return self._content_info_items