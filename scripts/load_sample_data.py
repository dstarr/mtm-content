from datetime import datetime
import random
from dotenv import load_dotenv
import os
import pymongo
import uuid

load_dotenv()

COSMOS_DB_CONNECTION_STRING = os.environ.get("COSMOS_DB_CONNECTION_STRING")
COSMOS_DB_NAME = os.environ.get("COSMOS_DB_NAME")
COSMOS_DB_CONTENT_COLLECTION_NAME = os.environ.get("COSMOS_DB_CONTENT_COLLECTION_NAME")
COSMOS_DB_METADATA_COLLECTION_NAME = os.environ.get("COSMOS_DB_METADATA_COLLECTION_NAME")

def make_playlists():
    playlists = {
        "name": "playlists",
        "playlists": [
            {"id": str(uuid.uuid4()), "name": "Doing business in the marketplace", "short_name": "The business of marketplace", "content": []},
            {"id": str(uuid.uuid4()), "name": "The marketplace for customers", "short_name": "For customers", "content": []},
            {"id": str(uuid.uuid4()), "name": "Mastering Container offers", "short_name": "Container offers", "content": []},
            {"id": str(uuid.uuid4()), "name": "Mastering Managed Application offers", "short_name": "Managed Application offers", "content": []},
            {"id": str(uuid.uuid4()), "name": "Mastering Partner Center", "short_name": "Partner Center", "content": []},
            {"id": str(uuid.uuid4()), "name": "Mastering SaaS Offers", "short_name": "SaaS Offers", "content": []},
            {"id": str(uuid.uuid4()), "name": "Mastering the SaaS Accelerator", "short_name": "SaaS Accelerator", "content": []},
            {"id": str(uuid.uuid4()), "name": "Mastering Virtual Machine offers", "short_name": "Virtual Machine offers", "content": []},
        ],
    }

    return playlists

def make_content():
    content_modules = []

    for i in range(1, 21):
        
        content = {
            "id": str(uuid.uuid4()),
            "title": f"Title {i}",
            "description": f"This is the {i} module",
            "youtube_url": f"https://www.youtube.com/watch?v={i}",
            "is_active": True,
            "date_created": datetime.utcnow(),
            "date_updated": datetime.utcnow(),
            "created_by": "David Starr"
        }

        content_modules.append(content)

    return content_modules

def assign_content_to_playlist(playlist, content):
    playlist["content"] = []
    
    count = 1
    for i in range(1, 6):
        content_item = random.choice(content)
        content_info = {
            "id": content_item["id"],
            "display_order": count
        }
        
        if _content_is_already_in_playlist(content_item, playlist):
            continue
        
        playlist["content"].append(content_info)
        count += 1

    return playlist

def write_content_to_mongo(content):
    client = pymongo.MongoClient(CUSTOMCONNSTR_COSMOS_DB_CONNECTION_STRING)
    db = client[COSMOS_DB_NAME]
    content_collection = db[COSMOS_DB_CONTENT_COLLECTION_NAME]

    content_collection.delete_many({})
    content_collection.insert_many(content)

    client.close()
    
def write_playlist_to_mongo(playlists):
    client = pymongo.MongoClient(CUSTOMCONNSTR_COSMOS_DB_CONNECTION_STRING)
    db = client[COSMOS_DB_NAME]
    metadata_collection = db[COSMOS_DB_METADATA_COLLECTION_NAME]

    metadata_collection.delete_many({})
    metadata_collection.insert_one(playlists)

    client.close()
    
def _content_is_already_in_playlist(content, playlist):
    for content_item in playlist["content"]:
        if content_item["id"] == content["id"]:
            return True
        
    return False

def _insert_sample_content_and_playlists():
    # ================================
    # put in sample content
    # ================================
    content = make_content()

    print("Adding content")
    write_content_to_mongo(content)
    
    # ================================
    # put in actual playlists
    # ================================
    playlists_with_content = []
    playlists_doc = make_playlists()

    for playlist in playlists_doc["playlists"]:
        playlist = assign_content_to_playlist(playlist, content)
        playlists_with_content.append(playlist)
        
    playlists_doc["playlists"] = playlists_with_content    
    
    print("Adding playlists")
    write_playlist_to_mongo(playlists_doc)

def _insert_playlist_only():
    playlists_doc = make_playlists()
    write_playlist_to_mongo(playlists_doc)

if __name__ == "__main__":

    # _insert_sample_content_and_playlists()
    
    _insert_playlist_only()

    

    
    