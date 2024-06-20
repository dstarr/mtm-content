# Mastering the Marketplace

The tools in this repository are used to manage the content for the Mastering the Marketplace program.

## MTM Contnent Manager

This Flask-based web application enables storing content such as video, slides, and provising data about the content, such as title and description.

```cmd
AZURE_TENANT_ID=
AZURE_CLIENT_ID=
AZURE_CLIENT_SECRET=

BLOB_STORAGE_CONNECTION_STRING=
BLOB_STORAGE_CONTAINER_NAME_SLIDES=slides
BLOB_STORAGE_CONTAINER_NAME_PDFS=pdfs
BLOB_STORAGE_CONTAINER_NAME_VIDEO=video
BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS=transcripts
BLOB_STORAGE_CONTAINER_NAME_SAMPLE_CODE=code

COSMOS_DB_CONNECTION_STRING=
COSMOS_DB_NAME=mtm-site
COSMOS_DB_CONTENT_COLLECTION_NAME=mtm-content
COSMOS_DB_METADATA_COLLECTION_NAME=mtm-meta-data

FLASK_DEBUG=1 
FLASK_PORT=5000
FLASK_SESSION_SECRET=
```

## Scripts

The Python scripts in this folder are used during development to manipulate data in the databases underlying thecontent management solution.

The scripts depend on the following environmental variables.

```cmd
AZURE_TENANT_ID=
AZURE_CLIENT_ID=
AZURE_CLIENT_SECRET=

BLOB_STORAGE_CONNECTION_STRING=
BLOB_STORAGE_CONTAINER_NAME_SLIDES=slides
BLOB_STORAGE_CONTAINER_NAME_PDFS=pdfs
BLOB_STORAGE_CONTAINER_NAME_VIDEO=video
BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS=transcripts
BLOB_STORAGE_CONTAINER_NAME_SAMPLE_CODE=code

COSMOS_DB_CONNECTION_STRING=
COSMOS_DB_NAME=mtm-site
COSMOS_DB_CONTENT_COLLECTION_NAME=mtm-content
COSMOS_DB_METADATA_COLLECTION_NAME=mtm-meta-data
```