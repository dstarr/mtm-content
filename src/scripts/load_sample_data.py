from datetime import datetime
import random
import time
from dotenv import load_dotenv
import os
import pymongo
import uuid

from azure.storage.blob import BlobServiceClient, PublicAccess

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

def get_playlists():
    playlists = {
        "name": "playlists",
        "playlists": [
            {"id": str(uuid.uuid4()), "name": "Mastering Container offers"},
            {"id": str(uuid.uuid4()), "name": "Mastering Managed Application offers"},
            {"id": str(uuid.uuid4()), "name": "Mastering Partner Center"},
            {"id": str(uuid.uuid4()), "name": "Mastering SaaS Offers"},
            {"id": str(uuid.uuid4()), "name": "Mastering Virtual Machine offers"},
            {"id": str(uuid.uuid4()), "name": "The marketplace for customers"},
            {"id": str(uuid.uuid4()), "name": "Business in the marketplace"},
        ],
    }

    return playlists

def get_modules(playlists, video_url, transcript_url, slides_url, pdf_url):
    modules = []

    for i in range(1, 10):
        
        playlist = random.choice(playlists["playlists"])

        module = {
            "id": str(uuid.uuid4()),
            "title": f"Title {i}",
            "description": f"This is the {i} module",
            "youtube_url": f"https://www.youtube.com/watch?v={i}",
            "tags": ["tag1", "tag2", "tag3"],
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
            "video_url": video_url,
            "transcript_url": transcript_url,
            "slides_url": slides_url,
            "pdf_url": pdf_url,
        }

        modules.append(module)

    return modules

def get_mongo_collections(db):
    
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

def write_mongo_data(video_url, transcript_url, slides_url, pdf_url):
    client = pymongo.MongoClient(COSMOS_DB_CONNECTION_STRING)
    db = client[COSMOS_DB_NAME]

    playlist_collection, content_collection = get_mongo_collections(db)
    
    # delete any existing data from mongo
    playlist_collection.delete_many({})
    content_collection.delete_many({})

    # playlists
    print("Creating playlists...")
    playlists = get_playlists()
    playlist_collection.insert_one(playlists)
    
    # content modules
    print("Creating content modules...")
    modules = get_modules(playlists, video_url, transcript_url, slides_url, pdf_url)
    content_collection.insert_many(modules)


    client.close()

def delete_blob_containers():

    blob_service_client = BlobServiceClient.from_connection_string(BLOB_STORAGE_CONNECTION_STRING)
    
    # List all containers in the blob service account
    containers = blob_service_client.list_containers()

    # Iterate through each container and delete
    for container in containers:
        
        container_name = container['name']
        container_client = blob_service_client.get_container_client(container_name)
    
        blob_service_client.delete_container(container_name)

        # Wait for the container to be deleted
        while True:
            if not container_client.exists():
                break
            time.sleep(1)  # Wait for 1 second before checking again

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

if __name__ == "__main__":

    video_url = upload_video()
    transcript_url = upload_transcript()
    slides_url = upload_slides()
    pdf_url = upload_pdf()

    write_mongo_data(video_url, transcript_url, slides_url, pdf_url)

    
    