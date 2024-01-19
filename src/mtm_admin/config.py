import os

from dotenv import load_dotenv

load_dotenv()

FLASK_DEBUG = os.environ.get("FLASK_DEBUG")
FLASK_PORT = os.environ.get("FLASK_PORT")

COSMOS_DB_CONNECTION_STRING = os.environ.get("COSMOS_DB_CONNECTION_STRING")
COSMOS_DB_NAME = os.environ.get("COSMOS_DB_NAME")
COSMOS_DB_CONTENT_COLLECTION_NAME = os.environ.get("COSMOS_DB_CONTENT_COLLECTION_NAME")
COSMOS_DB_METADATA_COLLECTION_NAME = os.environ.get("COSMOS_DB_METADATA_COLLECTION_NAME")


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

if env_vars_set == False:
    exit(1)
