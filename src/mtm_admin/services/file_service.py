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
        "content_key": "slide_url",
        "display_name": "Slides",
        "content_type": "slides"
    }
    TRANSCRIPT = {
        "container_name": config.BLOB_STORAGE_CONTAINER_NAME_TRANSCRIPTS,
        "content_key": "transcript_url",
        "display_name": "Transcript",
        "content_type": "transcript"
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
    OTHER = {
        "container_name": config.BLOB_STORAGE_CONTAINER_NAME_OTHER,
        "content_key": "other_url",
        "display_name": "Other",
        "content_type": "other"
    }

class FileService():
    def upload_to_blob(self, blob_name, content, file_type: FileType):
        try:
            blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_STORAGE_CONNECTION_STRING)

            blob_client = blob_service_client.get_blob_client(container=file_type.value["container_name"], blob=blob_name)

            blob_client.upload_blob(content, overwrite=True)

            return blob_client.url

        except Exception as ex:
            print('Exception:')
            print(ex)

    def get_blob_from_storage(self, blob_name, file_type: FileType):
        try:
            blob_client = BlobServiceClient.from_connection_string(config.BLOB_STORAGE_CONNECTION_STRING).get_blob_client(container=file_type, blob=blob_name)

            print(f"Downloading blob: {blob_name} from Azure Storage")
            blob_data = blob_client.download_blob().readall()
            print("Download successful")

            return blob_data

        except Exception as ex:
            print('Exception:')
            print(ex)

    def delete_blob_in_storage(self, file_type, blob_name):
        container_name = file_type.value["container_name"]
        try:
            blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_STORAGE_CONNECTION_STRING)
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

            if blob_client.exists():
                print(f"Deleting blob: {blob_name} from Azure Storage")
                blob_client.delete_blob()
                print("Deletion successful")

        except Exception as ex:
            print('Exception:')
            print(ex)
