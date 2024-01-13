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
    
    modules = []

    for i in range(1,10):
        module = {
            "id": str(uuid.uuid4()),
            "name": f"module-{i}",
            "title": f"Title {i}",
            "description": f"This is the {i} module",
            "youtube_url": f"https://www.youtube.com/watch?v={i}",
            "tags": ["python", "mongodb", "azure"],
            "playlist": f"Playlist {i}",
        }

        modules.append(module)

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

