from datetime import datetime
import random
import time
from dotenv import load_dotenv
import os
import pymongo
import uuid

from azure.storage.blob import BlobServiceClient, PublicAccess
from typing import List, Dict

load_dotenv()

COSMOS_DB_CONNECTION_STRING = os.environ.get("COSMOS_DB_CONNECTION_STRING")
COSMOS_DB_NAME = os.environ.get("COSMOS_DB_NAME")
COSMOS_DB_CONTENT_COLLECTION_NAME = os.environ.get("COSMOS_DB_CONTENT_COLLECTION_NAME")
COSMOS_DB_METADATA_COLLECTION_NAME = os.environ.get("COSMOS_DB_METADATA_COLLECTION_NAME")

BLOB_STORAGE_CONNECTION_STRING=os.environ.get("BLOB_STORAGE_CONNECTION_STRING")
BLOB_STORAGE_NAME=os.environ.get("BLOB_STORAGE_NAME")
BLOB_STORAGE_CONTAINER_NAME_SLIDES=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_SLIDES")
BLOB_STORAGE_CONTAINER_NAME_PDFS=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_PDFS")
BLOB_STORAGE_CONTAINER_NAME_VIDEO=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_VIDEO")
BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS")

FILE_DIR=os.environ.get("FILE_DIR")

def make_playlists():
    playlists = {
        "name": "playlists",
        "playlists": [
            {"id": str(uuid.uuid4()), "name": "Mastering Container offers", "short_name": "Container offers"},
            {"id": str(uuid.uuid4()), "name": "Mastering Managed Application offers", "short_name": "Managed Application offers"},
            {"id": str(uuid.uuid4()), "name": "Mastering Partner Center", "short_name": "Partner Center"},
            {"id": str(uuid.uuid4()), "name": "Mastering SaaS Offers", "short_name": "SaaS Offers"},
            {"id": str(uuid.uuid4()), "name": "Mastering Virtual Machine offers", "short_name": "Virtual Machine offers"},
            {"id": str(uuid.uuid4()), "name": "The marketplace for customers", "short_name": "For customers"},
            {"id": str(uuid.uuid4()), "name": "Doing business in the marketplace", "short_name": "Business in the marketplace"},
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

def upload_pdf():
    file_path=f"{FILE_DIR}/02.0-ma-overview.pdf"
    container_name=BLOB_STORAGE_CONTAINER_NAME_PDFS

    blob_url = upload_file_to_blob(file_path, container_name)

    return blob_url

def upload_slides():
    file_path=f"{FILE_DIR}/02.0-ma-overview.pptx"
    container_name=BLOB_STORAGE_CONTAINER_NAME_SLIDES

    blob_url = upload_file_to_blob(file_path, container_name)

    return blob_url
    
def upload_transcript():
    file_path=f"{FILE_DIR}/02.0-ma-overview-en-US.vtt"
    container_name=BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS

    blob_url = upload_file_to_blob(file_path, container_name)

    return blob_url

def upload_video():

    file_path=f"{FILE_DIR}/02.0-ma-overview.mp4"
    container_name=BLOB_STORAGE_CONTAINER_NAME_VIDEO

    blob_url = upload_file_to_blob(file_path, container_name)

    return blob_url

def upload_file_to_blob(file_path, container_name):
    print(f"Uploading {file_path} to {container_name}...")

    file_name = os.path.basename(file_path)

    blob_service_client = BlobServiceClient.from_connection_string(BLOB_STORAGE_CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    
    blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}/{file_name}"
    # https://dsmtmcontentmgmtstore.blob.core.windows.net/test-pdfs/02.0-ma-overview.pdf

    # create the container if it doesn't exist
    if not container_client.exists():
        blob_service_client.create_container(container_name)
        time.sleep(5)
        container_client = blob_service_client.get_container_client(container_name)
        container_client.set_container_access_policy(public_access=PublicAccess.CONTAINER)

    # upload the file
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    return blob_url

def assign_content_to_playlist(playlist, content):
    
    print(content)
    
    playlist["content"] = []

    for i in range(0, 5):
        item = random.choice(content)
        
        if item["id"] in playlist["content"]:
            continue
        
        item["display-order"] = i
        playlist["content"].append(item["id"])

    return playlist

def write_content_to_mongo(content):
    client = pymongo.MongoClient(COSMOS_DB_CONNECTION_STRING)
    db = client[COSMOS_DB_NAME]
    content_collection = db[COSMOS_DB_CONTENT_COLLECTION_NAME]

    content_collection.delete_many({})
    content_collection.insert_many(content)

    client.close()
    
def write_playlist_to_mongo(playlists):
    client = pymongo.MongoClient(COSMOS_DB_CONNECTION_STRING)
    db = client[COSMOS_DB_NAME]
    metadata_collection = db[COSMOS_DB_METADATA_COLLECTION_NAME]

    metadata_collection.delete_many({})
    metadata_collection.insert_one(playlists)

    client.close()
    

if __name__ == "__main__":

    # video_url = upload_video()
    # transcript_url = upload_transcript()
    # slides_url = upload_slides()
    # pdf_url = upload_pdf()

    # write_mongo_data(video_url, transcript_url, slides_url, pdf_url)

    content = make_content()
    print("Adding content")
    write_content_to_mongo(content)
    
    playlists_with_content = []
    playlists_doc = make_playlists()

    for playlist in playlists_doc["playlists"]:
        playlist = assign_content_to_playlist(playlist, content)
        playlists_with_content.append(playlist)
        
    playlists_doc["playlists"] = playlists_with_content    
    
    print("Adding playlists")
    write_playlist_to_mongo(playlists_doc)

    
    