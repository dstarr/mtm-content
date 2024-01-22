from datetime import datetime
import os
import uuid
import pymongo

import config


class ContentService:
    def __init__(self):
        pass

    def get_all_modules(self):
        _, content_collection = self.get_collections()

        modules = content_collection.find()

        return modules

    def get_module(self, module_id):
        _, content_collection = self.get_collections()

        module = content_collection.find_one({"id": module_id})

        return module

        # # get the playlist for the module
        # playlist = None
        # playlists_doc = metadata_collection.find_one({"name": "playlists"})
        # for playlist_doc in playlists_doc["playlists"]:
        #     if str(playlist_doc["id"]) == module["playlist_id"]:
        #         playlist = playlist_doc
        #         break

        # return {
        #     "module": module, 
        #     "playlist": playlist
        #     }

    def get_modules_for_playlist(self, playlist_id):
        _, content_collection = self.get_collections()

        modules = content_collection.find({"playlist_id": playlist_id})

        return modules

    def add_module(self, module):
        _, content_collection = self.get_collections()

        content_collection.insert_one(module)

    def update_module(self, module_id, module_to_update):

        _, content_collection = self.get_collections()

        content_collection.update_one({"id": module_id}, {"$set": module_to_update})

    def get_playlists(self):
        metadata_collection, _ = self.get_collections()

        playlists = metadata_collection.find_one({"name": "playlists"})

        return playlists["playlists"]

    def get_playlist(self, id):
        metadata_collection, _ = self.get_collections()

        playlist = metadata_collection.find_one(
            {
                "name": "playlists"
            }, 
            {
                "playlists": { "$elemMatch": {"id": id} }
            }
        )["playlists"][0]

        if playlist is None:
            raise Exception(f"Playlist with id {id} not found")

        return playlist

    def get_playlist_with_modules(self, id):
        metadata_collection, _ = self.get_collections()

        playlist = metadata_collection.find_one(
            {"name": "playlists"}, {"playlists": {"$elemMatch": {"id": id}}}
        )["playlists"][0]

        playlist["modules"] = self.get_modules_for_playlist(playlist["id"])

        return playlist

    def update_playlist(self, id, name):
        metadata_collection, _ = self.get_collections()

        playlists_doc = metadata_collection.find_one({"name": "playlists"})

        for playlist in playlists_doc["playlists"]:
            if str(playlist["id"]) == id:
                playlist["name"] = name
                break

        metadata_collection.update_one({"name": "playlists"}, {"$set": playlists_doc})

    def get_collections(self):
        client = pymongo.MongoClient(config.COSMOS_DB_CONNECTION_STRING)
        db = client[config.COSMOS_DB_NAME]

        content_collection = db[config.COSMOS_DB_CONTENT_COLLECTION_NAME]
        metadata_collection = db[config.COSMOS_DB_METADATA_COLLECTION_NAME]

        # create the collection if it does not exist
        if db[config.COSMOS_DB_CONTENT_COLLECTION_NAME] is None:
            content_collection = db.create_collection(
                name=config.COSMOS_DB_CONTENT_COLLECTION_NAME
            )
        else:
            content_collection = db[config.COSMOS_DB_CONTENT_COLLECTION_NAME]

        # create the collection if it does not exist
        if db[config.COSMOS_DB_METADATA_COLLECTION_NAME] is None:
            metadata_collection = db.create_collection(
                name=config.COSMOS_DB_METADATA_COLLECTION_NAME
            )
        else:
            metadata_collection = db[config.COSMOS_DB_METADATA_COLLECTION_NAME]

        return metadata_collection, content_collection
