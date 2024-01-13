from dotenv import load_dotenv
import os
import pymongo
import uuid

load_dotenv()

COSMOS_CONNECTION_STRING = os.environ.get("COSMOS_CONNECTION_STRING")
COSMOS_DB_NAME = os.environ.get("COSMOS_DB_NAME")
COSMOS_DB_COLLECTION_NAME = os.environ.get("COSMOS_DB_COLLECTION_NAME")

print(f"DB NAME: {COSMOS_DB_NAME}")
print(f"COLLECTION NAME: {COSMOS_DB_COLLECTION_NAME}")

def get_modules():
    modules = [
        {
            "id": str(uuid.uuid4()),
            "name": "module-1",
            "description": "This is the first module",
            "youtube_url": "https://www.youtube.com/watch?v=9bZkp7q19f0",
            "tags": ["python", "mongodb", "azure"],
            "playlist": "Playlist 1",
        },
        {
            "id": str(uuid.uuid4()),
            "name": "module-2",
            "description": "This is the 2nd module",
            "youtube_url": "https://www.youtube.com/watch?v=foo",
            "tags": ["python", "mongodb"],
            "playlist": "Playlist 2",
        }
    ]

    return modules
    
client = pymongo.MongoClient(COSMOS_CONNECTION_STRING)
db = client['mtmcontent']

# create the collection if it does not exist
if db["COSMOS_DB_COLLECTION_NAME"] is None:
    collection = db.create_collection(name=COSMOS_DB_COLLECTION_NAME)
else:
    collection = db[COSMOS_DB_COLLECTION_NAME]

# delete any existing data
collection.delete_many({})

# create a module to insert
modules = get_modules()

collection.insert_many(modules)

client.close()

