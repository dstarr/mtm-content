from enum import Enum
from azure.storage.blob import BlobServiceClient
import config

class FileType(Enum):
    PDF = {
        "container_name": config.BLOB_STORAGE_CONTAINER_NAME_PDFS,
        "content_key": "pdf_url",
        "display_name": "PDF",
        "content_type": "pdf"
    }
    SLIDE = {
        "container_name": config.BLOB_STORAGE_CONTAINER_NAME_SLIDES,
        "content_key": "slides_url",
        "display_name": "Slides",
        "content_type": "slides"
    }
    VIDEO = {
        "container_name": config.BLOB_STORAGE_CONTAINER_NAME_VIDEO,
        "content_key": "video_url",
        "display_name": "Video",
        "content_type": "video"
    }
    SAMPLE_CODE = {
        "container_name": config.BLOB_STORAGE_CONTAINER_NAME_SAMPLE_CODE,
        "content_key": "sample_code_url",
        "display_name": "Sample code",
        "content_type": "sample_code"
    }
    
class FileService():
    def upload_to_blob(self, blob_name, content, file_type: FileType):
        
        container_name = file_type.value["container_name"]
        
        blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_STORAGE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(container_name)
        
        # ensure the container exists
        if not container_client.exists():
            container_client.create_container()
        
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        blob_client.upload_blob(content, overwrite=True)

        return blob_client.url

    def get_blob_from_storage(self, blob_name, file_type: FileType):
        blob_client = BlobServiceClient.from_connection_string(config.BLOB_STORAGE_CONNECTION_STRING).get_blob_client(container=file_type, blob=blob_name)

        print(f"Downloading blob: {blob_name} from Azure Storage")
        blob_data = blob_client.download_blob().readall()
        print("Download successful")

        return blob_data

    def delete_blob_in_storage(self, blob_name, file_type: FileType):
        container_name = file_type.value["container_name"]
        blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        if blob_client.exists():
            print(f"Deleting blob: {blob_name} from Azure Storage")
            blob_client.delete_blob()
            print("Deletion successful")