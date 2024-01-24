class PlaylistDetailModel():
    
    def __init__(self, playlist, content):
        self.playlist = playlist
        self.content = content
        
    def get_playlist(self):
        return self.playlist
    
    def get_content(self):
        return self.content