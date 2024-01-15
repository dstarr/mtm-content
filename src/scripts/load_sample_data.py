from datetime import datetime
import random
from dotenv import load_dotenv
import os
import pymongo
import uuid

load_dotenv()

COSMOS_CONNECTION_STRING = os.environ.get("COSMOS_CONNECTION_STRING")
COSMOS_DB_NAME = os.environ.get("COSMOS_DB_NAME")
COSMOS_DB_CONTENT_COLLECTION_NAME = os.environ.get("COSMOS_DB_CONTENT_COLLECTION_NAME")
COSMOS_DB_METADATA_COLLECTION_NAME = os.environ.get("COSMOS_DB_METADATA_COLLECTION_NAME")

print(f"DB NAME: {COSMOS_DB_NAME}")
print(f"COLLECTION NAME: {COSMOS_DB_CONTENT_COLLECTION_NAME}")


def get_playlists():
    playlists = {
        "name": "playlists",
        "playlists": [
            {"id": str(uuid.uuid4()), "name": "Mastering Container offers"},
            {"id": str(uuid.uuid4()), "name": "Mastering Managed Application offers"},
            {"id": str(uuid.uuid4()), "name": "Mastering Partner Center"},
            {"id": str(uuid.uuid4()), "name": "Mastering SaaS Offers"},
            {"id": str(uuid.uuid4()), "name": "Mastering Virtual Machine offers"},
        ],
    }

    return playlists

def get_collections(db):
    
    # create the collection if it does not exist
    if db["COSMOS_DB_CONTENT_COLLECTION_NAME"] is None:
        content_collection = db.create_collection(name=COSMOS_DB_CONTENT_COLLECTION_NAME)
    else:
        content_collection = db[COSMOS_DB_CONTENT_COLLECTION_NAME]
        
    # create the collection if it does not exist
    if db["COSMOS_DB_METADATA_COLLECTION_NAME"] is None:
        metadata_collection = db.create_collection(name=COSMOS_DB_METADATA_COLLECTION_NAME)
    else:
        metadata_collection = db[COSMOS_DB_METADATA_COLLECTION_NAME]
    
    return metadata_collection, content_collection
    
def get_modules(playists):
    modules = []

    for i in range(1, 10):
        
        playlist = random.choice(playlists["playlists"])

        module = {
            "id": str(uuid.uuid4()),
            "name": f"module-{i}",
            "title": f"Title {i}",
            "description": f"This is the {i} module",
            "youtube_url": f"https://www.youtube.com/watch?v={i}",
            "tags": ["python", "mongodb", "azure"],
            "playlist_id": playlist["id"],
            "date_created": datetime.strptime(
                str(datetime(2024, 1, 1)), "%Y-%m-%d %H:%M:%S"
            ),
            "date_updated": datetime.strptime(
                str(datetime(2024, 2, 1)), "%Y-%m-%d %H:%M:%S"
            ),
            "created_by": "David Starr",
            "updated_by": "Elle Starr",
            "is_active": True,
        }

        modules.append(module)

    return modules


if __name__ == "__main__":

    client = pymongo.MongoClient(COSMOS_CONNECTION_STRING)
    db = client[COSMOS_DB_NAME]

    playlist_collection, content_collection = get_collections(db)
    
    # delete any existing data
    playlist_collection.delete_many({})
    content_collection.delete_many({})

    # playlists
    playlists = get_playlists()
    playlist_collection.insert_one(playlists)
    
    # content modules
    modules = get_modules(playlists)
    content_collection.insert_many(modules)


    client.close()
