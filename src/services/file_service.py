import datetime
from enum import Enum
from azure.storage.blob import BlobServiceClient, PublicAccess, AccessPolicy, ResourceTypes, AccountSasPermissions, generate_account_sas
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
        
        # set up client
        blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_STORAGE_CONNECTION_STRING)
        
        # create the container if it doesn't exist
        if container_name not in [container.name for container in blob_service_client.list_containers()]:
            
            access_policy = AccessPolicy(permission=AccountSasPermissions(read=True), expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=1))
            identifiers = {'id': access_policy}
            
            container_client = blob_service_client.create_container(container_name)
            container_client.set_container_access_policy(public_access=PublicAccess.Blob, signed_identifiers=identifiers)
        
        # upload the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        try:
            blob_client.upload_blob(content, overwrite=True, timeout=300)
        except Exception as e:
            print(e)
            raise Exception(f"Error uploading blob {blob_name} to container {container_name}")
        
        print(f"DONE")

        return blob_client.url

    def get_blob_from_storage(self, blob_name, file_type: FileType):
        blob_client = BlobServiceClient.from_connection_string(config.BLOB_STORAGE_CONNECTION_STRING).get_blob_client(container=file_type, blob=blob_name)

        blob_data = blob_client.download_blob().readall()

        return blob_data

    def delete_blob_in_storage(self, blob_name, file_type: FileType):
        container_name = file_type.value["container_name"]
        blob_service_client = BlobServiceClient.from_connection_string(config.BLOB_STORAGE_CONNECTION_STRING)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

        if blob_client.exists():
            blob_client.delete_blob()
            
    def delete_all_blobs_for_content(self, content):
        
        if content.get("video_url") is not None:
            self.delete_blob_in_storage(file_type=FileType.VIDEO, blob_name=content["video_url"].split("/")[-1])
        if content.get("slides_url") is not None:
            self.delete_blob_in_storage(file_type=FileType.SLIDE, blob_name=content["slides_url"].split("/")[-1])
        if content.get("pdf_url") is not None:
            self.delete_blob_in_storage(file_type=FileType.PDF, blob_name=content["pdf_url"].split("/")[-1])
        if content.get("sample_code_url") is not None:
            self.delete_blob_in_storage(file_type=FileType.SAMPLE_CODE, blob_name=content["sample_code_url"].split("/")[-1])
        