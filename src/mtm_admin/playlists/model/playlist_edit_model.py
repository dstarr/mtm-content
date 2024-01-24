class PlaylistEditModel():
    
    def __init__(self, playlist, content_info):
        self.playlist = playlist
        self.content_info = content_info
        
    def get_playlist(self):
        return self.playlist
    
    def get_content_info(self):
        return self.content_info