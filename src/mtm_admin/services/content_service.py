from datetime import datetime
import os
import uuid
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
    
    def update_module(self, new_values):
        _, content_collection = self.get_collections()
        
        module = content_collection.find_one({"id": new_values["id"]})

        is_active = False
        if new_values.get("is_active") == "True":
            is_active = True
        
        module["title"] = new_values["title"]
        module["description"] = new_values["description"]
        module["playlist_id"] = new_values["playlist_id"]
        module["is_active"] = is_active
        module["date_updated"] = datetime.utcnow()
        module["updated_by"] = "Julio Colon"
        
        content_collection.update_one({"id": new_values["id"]}, {"$set": module})
    
    def get_playlists(self):
        metadata_collection, _ = self.get_collections()

        playlists = metadata_collection.find_one({"name": "playlists"})
        
        return playlists["playlists"]
    
    def get_playlist(self, id):
        metadata_collection, _ = self.get_collections()

        playlist = metadata_collection.find_one(
            { "name": "playlists" },
            { "playlists": { "$elemMatch": { "id": id } } }
        )["playlists"][0]

        playlist["modules"] = self.get_modules_for_playlist(playlist["id"])

        return playlist
    
    def get_modules_for_playlist(self, playlist_id):
        _, content_collection = self.get_collections()

        modules = content_collection.find({ "playlist_id": playlist_id })

        return modules

    def add_module(self, new_values):
        _, content_collection = self.get_collections()
        
        module = {
            "id": str(uuid.uuid4()),
            "title": new_values["title"],
            "description": new_values["description"],
            "playlist_id": new_values["playlist_id"],
            "is_active": new_values["is_active"],
            "date_created": datetime.utcnow(),
            "date_updated": datetime.utcnow(),
            "created_by": "David",
            "updated_by": "Julio"
            
        }
        
        # add the module to the collection
        content_collection.insert_one(module)
        
        return self.get_module(module["id"])
    
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
