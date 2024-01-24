from datetime import datetime
import uuid
from flask import Blueprint, redirect, render_template, request, url_for
from services.file_service import FileService, FileType
from services.content_service import ContentService
from content.models.detail_model import DetailModel
from content.models.edit_model import EditModel

content_bp = Blueprint(
    "content", __name__, 
    template_folder="templates",
    static_folder="static",
)

content_service = ContentService()
file_service = FileService()


@content_bp.route('add', methods=['GET','POST'])
def content_add():
    if request.method == 'GET':
        playlists=content_service.get_playlists()
        return render_template('contents_add.html', playlists=playlists)
    
    elif request.method == 'POST':

        property_values=request.form

        is_active = False
        if property_values.get("is_active"):
            is_active = True

        content = {
            "id": str(uuid.uuid4()),

            "created_by": "",
            "date_created": datetime.utcnow(),
            "date_updated": datetime.utcnow(),
            "updated_by": "",

            "notes": property_values["notes"],
            "description": property_values["description"],
            "is_active": is_active,
            "playlist_id": property_values["playlist_id"],
            "title": property_values["title"],
            "youtube_url": property_values["youtube_url"],
        }

        content_service.add_content(content=content)

        return redirect(url_for('content.content_detail', content_id=content["id"]))

@content_bp.route('detail/<content_id>')
def content_detail(content_id):
    content = content_service.get_content(content_id)
    content_playlists = content_service.get_playlists_for_content(content_id)
    
    model = DetailModel(content=content, playlists=content_playlists)

    return render_template('content_detail.html', model=model)

@content_bp.route('edit/<content_id>', methods=['GET', 'POST'])
def content_edit(content_id):
    
    if request.method == 'POST':
        property_values=request.form

        # save changes to the content
        content = content_service.get_content(content_id)
        new_content_entity = map_content_entity(content=content, property_values=property_values)
        content_service.update_content(content_to_update=new_content_entity)

        # save changes to the playlists
        playlist_ids = property_values.getlist('playlist_id')
        content_service.update_playlist_names_for_content(content_id=content_id, playlist_ids=playlist_ids)

        return redirect(url_for('content.content_detail', content_id=content_id))

    # render the edit form
    elif request.method == 'GET':
        content = content_service.get_content(content_id)
        playlists = content_service.get_playlists()
        model = EditModel(playlists=playlists, content=content)
    
        return render_template('content_edit.html', model=model)

def map_content_entity(content, property_values):

    is_active = False
    if property_values.get("is_active"):
        is_active = True
            
    content["date_updated"] = datetime.utcnow()
    content["description"] = property_values["description"]
    content["is_active"] = is_active
    content["notes"] = property_values["notes"]
    content["playlist_id"] = property_values["playlist_id"]
    content["title"] = property_values["title"]
    content["updated_by"] = ""
    return content
    
@content_bp.route('add_attachment', methods=['POST'])
def content_attachment_add():
    # Check if the 'file' key is present in request.files
    if not request.files['file']:
        print('No file in the request')
        raise Exception('No file in the request')
    
    content_id = request.form["content_id"]
    attachment_type = request.form["attachment_type"]
    
    # get the files from the request and upload them to blob storage
    file = request.files['file']
    file_name = file.filename
    file_contents = file.read()
    file_type = find_enum_by_container_key_value(key='content_type', value=attachment_type)

    blob_url = file_service.upload_to_blob(blob_name=file_name, content=file_contents, file_type=file_type)

    # add the data about the uploaded files to the content
    content = content_service.get_content(content_id)
    print("======   content   ======")           
    print(file_type.value["content_key"])

    content[file_type.value["content_key"]] = blob_url
    content_service.update_content(content_id=content_id, content_to_update=content)
    
    return redirect(request.referrer)

@content_bp.route('delete_attachment', methods=['POST'])
def content_attachment_delete():
    content_id = request.form["content_id"]
    blob_url = request.form["blob_url"]
    container_name = blob_url.split("/")[-2]
    blob_name=blob_url.split("/")[-1]
    file_type = find_enum_by_container_key_value(key='container_name', value=container_name)

    # remove the attachment from the content
    content = content_service.get_content(content_id)
    content[file_type.value["content_key"]] = None
    content_service.update_content(content_id=content_id, content_to_update=content)

    # delete the attachment from blob storage
    file_service.delete_blob_in_storage(file_type=file_type, blob_name=blob_name)

    return redirect(request.referrer)

def find_enum_by_container_key_value(key, value):
    for file_type in FileType:
        if file_type.value[key] == value:
            return file_type
    
    return None

