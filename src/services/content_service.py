import uuid
import pymongo
import config


class ContentService:
    def __init__(self):
        pass

    def get_all_content(self):
        _, content_collection = self._get_collections()

        contents = content_collection.find()
        
        return contents

    def get_content(self, content_id, content_collection=None):
        if content_collection is None:
            _, content_collection = self._get_collections()

        content = content_collection.find_one({"id": content_id})

        return content

    def get_playlists_for_content(self, content_id):
        all_playlists = self.get_playlists()
        
        content_playlists = []

        # if the content is in the playlist, add it to the list
        for playlist in all_playlists:
            for playlist_item in playlist["content"]:
                if playlist_item["id"] == content_id:
                    content_playlists.append(playlist)
                
        return content_playlists
        
    def update_playlists_content(self, content_id, playlist_ids):

        metadata_collection, _ = self._get_collections()
        playlists_doc = metadata_collection.find_one({"name": "playlists"})
        
        new_content_item = {
            "id": content_id,
            "display_order": 999
        }
        
        # remove the content from all playlists
        for playlist in playlists_doc["playlists"]:
            if playlist["content"] is not None:
                playlist["content"] = [item for item in playlist["content"] if item["id"] != content_id]
        
        # if a playlist is in the list of playlists to add the content to, add it
        for playlist in playlists_doc["playlists"]:
            if playlist["id"] in playlist_ids:
                playlist["content"].append(new_content_item)
            
        metadata_collection.update_one({"name": "playlists"}, {"$set": playlists_doc})

    def add_content(self, content):
        _, content_collection = self._get_collections()

        content_collection.insert_one(content)

    def update_content(self, content_to_update):

        _, content_collection = self._get_collections()

        content_id = content_to_update["id"]
        content_collection.update_one({"id": content_id}, {"$set": content_to_update})

    def get_playlists(self):
        metadata_collection, _ = self._get_collections()

        playlists = metadata_collection.find_one({"name": "playlists"})

        return playlists["playlists"]

    def create_playlist(self, name, short_name, description):
        metadata_collection, _ = self._get_collections()

        playlists_doc = metadata_collection.find_one({"name": "playlists"})

        new_playlist = {
            "id": str(uuid.uuid4()),
            "name": name,
            "short_name": short_name,
            "description": description,
            "content": []
        }

        playlists_doc["playlists"].append(new_playlist)

        metadata_collection.update_one({"name": "playlists"}, {"$set": playlists_doc})

    def get_playlist(self, id):
        metadata_collection, _ = self._get_collections()

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

    def get_playlist_with_contents(self, id):
        metadata_collection, content_collection = self._get_collections()

        playlist = metadata_collection.find_one(
            {"name": "playlists"}, {"playlists": {"$elemMatch": {"id": id}}}
        )["playlists"][0]

        ordered_content_items = sorted(playlist["content"], key=lambda x: x['display_order'])

        content_items = []
        for content_item in ordered_content_items:
            content = self.get_content(content_id=content_item['id'], content_collection=content_collection)
            content_items.append(
                { "id": content["id"], "title": content["title"], "display_order": content_item["display_order"] }
            )
            
        playlist["content"] = content_items



        return playlist

    def update_playlist(self, id, name, short_name, description):
        metadata_collection, _ = self._get_collections()

        playlists_doc = metadata_collection.find_one({"name": "playlists"})

        for playlist in playlists_doc["playlists"]:
            if str(playlist["id"]) == id:
                playlist["name"] = name
                playlist["short_name"] = short_name
                playlist["description"] = description
                break

        metadata_collection.update_one({"name": "playlists"}, {"$set": playlists_doc})

    def update_playlist_content_display_order(self, playlist_id, content_items):
        metadata_collection, _ = self._get_collections()

        playlists_doc = metadata_collection.find_one({"name": "playlists"})

        for playlist in playlists_doc["playlists"]:
            if str(playlist["id"]) == playlist_id:
                playlist["content"] = content_items
                break
        
        metadata_collection.update_one({"name": "playlists"}, {"$set": playlists_doc})

    def delete_content(self, content_id):
        meta_data_collection, content_collection = self._get_collections()
        
        # delete the content from any playlists
        playlists = self.get_playlists()
        for playlist in playlists:
            content_to_keep = [item for item in playlist["content"] if item["id"] != content_id]
            playlist["content"] = content_to_keep
        
        # write the updated playlists doc back to the database
        meta_data_collection.update_one({"name": "playlists"}, {"$set": {"playlists": playlists}})
        
        # delete the actual content
        content_collection.delete_one({"id": content_id})

    def _get_collections(self):
        
        client = pymongo.MongoClient(config.CUSTOMCONNSTR_COSMOS_DB_CONNECTION_STRING)
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

