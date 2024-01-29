import os

from dotenv import load_dotenv

load_dotenv()

FLASK_DEBUG=os.environ.get("FLASK_DEBUG")
FLASK_PORT=os.environ.get("FLASK_PORT")

AZURE_TENANT_ID=os.environ.get("AZURE_TENANT_ID")
AZURE_CLIENT_ID=os.environ.get("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET=os.environ.get("AZURE_CLIENT_SECRET")
AZURE_AUTHORITY = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
AZURE_REDIRECT_PATH = "/content/"
AZURE_ENDPOINT = 'https://graph.microsoft.com/v1.0/users'
AZURE_SCOPE = ["User.Read"]

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
BLOB_STORAGE_CONTAINER_NAME_SAMPLE_CODE=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_SAMPLE_CODE")
BLOB_STORAGE_CONTAINER_NAME_OTHER=os.environ.get("BLOB_STORAGE_CONTAINER_NAME_OTHER")

env_vars_set = True

if FLASK_DEBUG == None:
    FLASK_DEBUG=1

if FLASK_PORT == None:
    FLASK_PORT=5000

if AZURE_TENANT_ID == None:
    print("AZURE_TENANT_ID is not set")
    env_vars_set = False
    
if AZURE_AUTHORITY == None:
    print("AZURE_AUTHORITY is not set")
    env_vars_set = False

if AZURE_CLIENT_ID == None:
    print("AZURE_CLIENT_ID is not set")
    env_vars_set = False
    
if AZURE_CLIENT_SECRET == None:
    print("AZURE_CLIENT_SECRET is not set")
    env_vars_set = False

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

if BLOB_STORAGE_CONNECTION_STRING == None:
    print("BLOB_STORAGE_CONNECTION_STRING is not set")
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

if BLOB_STORAGE_CONTAINER_NAME_SAMPLE_CODE == None:
    print("BLOB_STORAGE_CONTAINER_NAME_SAMPLE_CODE is not set")
    env_vars_set = False

if env_vars_set == False:
    exit(1)
    
def _print_env_vars():
    for key, value in os.environ.items():
        print(f'{key}: {value}')
        
    print("AZURE_AUTHORITY: " + AZURE_AUTHORITY)
    
# _print_env_vars()
