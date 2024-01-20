import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import config

def upload_file_to_blob(blob_name, file):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_STORAGE_CONNCECTION_STRING)

        blob_client = blob_service_client.get_blob_client(container=config.BLOB_STORAGE_CONTAINER_NAME_VIDEO, blob=blob_name)

        print(f"Uploading {blob_name} to Azure Storage")

        # Upload the created file
        blob_client.upload_blob(file)

        print("Upload successful")
    except Exception as ex:
        print('Exception:')
        print(ex)

def download_blob_from_storage(blob_name, download_file_path, container_name, connection_string):
    try:
        # Create a blob client
        blob_client = BlobServiceClient.from_connection_string(connection_string).get_blob_client(container=container_name, blob=blob_name)

        print(f"Downloading blob: {blob_name} from Azure Storage")

        # Download the blob
        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob().readall())

        print("Download successful")
    except Exception as ex:
        print('Exception:')
        print(ex)

def delete_blob_in_storage(blob_name, container_name, connection_string):
    try:
        # Create a blob client
        blob_client = BlobServiceClient.from_connection_string(connection_string).get_blob_client(container=container_name, blob=blob_name)

        print(f"Deleting blob: {blob_name} from Azure Storage")

        # Delete the blob
        blob_client.delete_blob()

        print("Deletion successful")
    except Exception as ex:
        print('Exception:')
        print(ex)

def main():
    # Get environment variables
    BLOB_STORAGE_KEY = os.environ.get("BLOB_STORAGE_KEY")
    BLOB_STORAGE_NAME = os.environ.get("BLOB_STORAGE_NAME")
    BLOB_STORAGE_CONTAINER_NAME_VIDEO = os.environ.get("BLOB_STORAGE_CONTAINER_NAME_VIDEO")

    # Ensure variables are set
    if not all([BLOB_STORAGE_KEY, BLOB_STORAGE_NAME, BLOB_STORAGE_CONTAINER_NAME_VIDEO]):
        print("One or more environment variables are missing")
        return

    # Connection string
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={BLOB_STORAGE_NAME};AccountKey={BLOB_STORAGE_KEY};EndpointSuffix=core.windows.net"

    # Path to the local file to upload
    file_path = "path_to_video.mp4"
    blob_name = os.path.basename(file_path)  # Use the file name as the blob name

    # Upload the file
    upload_file_to_blob(file_path, BLOB_STORAGE_CONTAINER_NAME_VIDEO, blob_name, connection_string)

if __name__ == "__main__":
    main()
