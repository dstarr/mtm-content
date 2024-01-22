from enum import Enum
from azure.storage.blob import BlobServiceClient
import config

class FileType(Enum):
    PDF = {
        "container_name": config.BLOB_STORAGE_CONTAINER_NAME_PDFS,
        "content_key": "pdf_url",
        "display_name": "PDF"
    }
    SLIDE = {
        "container_name": config.BLOB_STORAGE_CONTAINER_NAME_SLIDES,
        "content_key": "slide_url",
        "display_name": "Slide"
    }
    TRANSCRIPT = {
        "container_name": config.BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS,
        "content_key": "transcript_url",
        "display_name": "Transcript"
    }
    VIDEO = {
        "container_name": config.BLOB_STORAGE_CONTAINER_NAME_VIDEO,
        "content_key": "video_url",
        "display_name": "Video"
    }

    OTHER = {
        "container_name": config.BLOB_STORAGE_CONTAINER_NAME_OTHER,
        "content_key": "other_url",
        "display_name": "Other"
    }

class FileService():
    def upload_to_blob(self, blob_name, content, file_type: FileType):
        try:
            blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_STORAGE_CONNCECTION_STRING)

            blob_client = blob_service_client.get_blob_client(container=file_type.value["container_name"], blob=blob_name)

            blob_client.upload_blob(content, overwrite=True)

            return blob_client.url

        except Exception as ex:
            print('Exception:')
            print(ex)

    def get_blob_from_storage(self, blob_name, file_type: FileType):
        try:
            blob_client = BlobServiceClient.from_connection_string(config.BLOB_STORAGE_CONNCECTION_STRING).get_blob_client(container=file_type, blob=blob_name)

            print(f"Downloading blob: {blob_name} from Azure Storage")
            blob_data = blob_client.download_blob().readall()
            print("Download successful")

            return blob_data

        except Exception as ex:
            print('Exception:')
            print(ex)

    def delete_blob_in_storage(self, blob_name, file_type: FileType):
        try:
            blob_client = BlobServiceClient.from_connection_string(config.BLOB_STORAGE_CONNCECTION_STRING).get_blob_client(container=file_type, blob=blob_name)

            print(f"Deleting blob: {blob_name} from Azure Storage")
            blob_client.delete_blob()
            print("Deletion successful")

        except Exception as ex:
            print('Exception:')
            print(ex)
