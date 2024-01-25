class PlaylistDetailModel():
    
    def __init__(self, playlist, content_info_items):
        self.playlist = playlist
        self.content_info_items = content_info_items
        
    def get_playlist(self):
        return self.playlist
    
    def get_content(self):
        return self.content_info_items