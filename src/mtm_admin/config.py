import os

from dotenv import load_dotenv

load_dotenv()

FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
FLASK_PORT = os.environ.get("FLASK_PORT")

COSMOS_DB_CONNECTION_STRING = os.environ.get("COSMOS_DB_CONNECTION_STRING")
COSMOS_DB_NAME = os.environ.get("COSMOS_DB_NAME")
COSMOS_DB_CONTENT_COLLECTION_NAME = os.environ.get("COSMOS_DB_CONTENT_COLLECTION_NAME")
COSMOS_DB_METADATA_COLLECTION_NAME = os.environ.get("COSMOS_DB_METADATA_COLLECTION_NAME")

BLOB_STORAGE_CONNCECTION_STRING=os.environ.get("BLOB_STORAGE_CONNCECTION_STRING")
BLOB_STORAGE_NAME=os.environ.get("BLOB_STORAGE_NAME")
BLOB_STORAGE_CONTAINER_NAME_SLIDES=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_SLIDES")
BLOB_STORAGE_CONTAINER_NAME_PDFS=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_PDFS")
BLOB_STORAGE_CONTAINER_NAME_VIDEO=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_VIDEO")
BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS")
BLOB_STORAGE_CONTAINER_NAME_OTHER=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_OTHER")

env_vars_set = True

if FLASK_DEBUG == None:
    FLASK_DEBUG = 0

if FLASK_PORT == None:
    FLASK_PORT = 3000

if COSMOS_DB_CONNECTION_STRING == None:
    print("COSMOS_DB_CONNECTION_STRING is not set")
    env_vars_set = False

if COSMOS_DB_NAME == None:
    print("COSMOS_DB_NAME is not set")
    env_vars_set = False

if COSMOS_DB_CONTENT_COLLECTION_NAME == None:
    print("COSMOS_DB_CONTENT_COLLECTION_NAME is not set")
    env_vars_set = False

if COSMOS_DB_METADATA_COLLECTION_NAME == None:
    print("COSMOS_DB_METADATA_COLLECTION_NAME is not set")
    env_vars_set = False

if BLOB_STORAGE_CONNCECTION_STRING == None:
    print("BLOB_STORAGE_CONNCECTION_STRING is not set")
    env_vars_set = False

if BLOB_STORAGE_NAME == None:
    print("BLOB_STORAGE_NAME is not set")
    env_vars_set = False

if BLOB_STORAGE_CONTAINER_NAME_SLIDES == None:
    print("BLOB_STORAGE_CONTAINER_NAME_SLIDES is not set")
    env_vars_set = False

if BLOB_STORAGE_CONTAINER_NAME_PDFS == None:
    print("BLOB_STORAGE_CONTAINER_NAME_PDFS is not set")
    env_vars_set = False

if BLOB_STORAGE_CONTAINER_NAME_VIDEO == None:
    print("BLOB_STORAGE_CONTAINER_NAME_VIDEO is not set")
    env_vars_set = False

if BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS == None:
    print("BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS is not set")
    env_vars_set = False

if BLOB_STORAGE_CONTAINER_NAME_OTHER == None:
    print("BLOB_STORAGE_CONTAINER_NAME_OTHER is not set")
    env_vars_set = False

if env_vars_set == False:
    exit(1)
