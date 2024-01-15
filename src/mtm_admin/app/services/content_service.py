import os
import pymongo

class ContentService:
    
    def __init__(self):
        self.connection_string = os.environ.get("COSMOS_DB_CONNECTION_STRING")
        self.db_name = os.environ.get("COSMOS_DB_NAME")
        self.content_collection_name = os.environ.get("COSMOS_DB_CONTENT_COLLECTION_NAME")
        self.metadata_collection_name = os.environ.get("COSMOS_DB_METADATA_COLLECTION_NAME")

    def get_all_modules(self):
        _, content_collection = self.get_collections()
    
        modules = content_collection.find()
        
        return modules
    
    def get_module(self, module_id):
        metadata_collection, content_collection = self.get_collections()

        # get the module
        module = content_collection.find_one({"id": module_id})
        
        # get the playlist for the module
        playlists_doc = metadata_collection.find_one({"name": "playlists"})

        playlist = None
        for playlist_doc in playlists_doc["playlists"]:
            if str(playlist_doc["id"]) == module["playlist_id"]:
                playlist = playlist_doc
                break
        
        return {
            "module": module,
            "playlist": playlist
        }
    
    def get_playlists(self):
        metadata_collection, _ = self.get_collections()

        playlists = metadata_collection.find_one({"name": "playlists"})
        
        return playlists["playlists"]
    
    def get_collections(self):
        client = pymongo.MongoClient(self.connection_string)
        db = client[self.db_name]
        
        content_collection = db[self.content_collection_name]
        metadata_collection = db[self.metadata_collection_name]
        
        # create the collection if it does not exist
        if db[self.content_collection_name] is None:
            content_collection = db.create_collection(name=self.content_collection_name)
        else:
            content_collection = db[self.content_collection_name]
            
        # create the collection if it does not exist
        if db[self.metadata_collection_name] is None:
            metadata_collection = db.create_collection(name=self.metadata_collection_name)
        else:
            metadata_collection = db[self.metadata_collection_name]
            
        return metadata_collection, content_collection
