from datetime import datetime
import uuid
from flask import Blueprint, redirect, render_template, request, url_for
from services.file_service import FileService, FileType
from services.content_service import ContentService
from modules.models.detail_model import DetailModel
from modules.models.edit_model import EditModel

modules_bp = Blueprint(
    "modules", __name__, 
    template_folder="templates",
    static_folder="static",
)

content_service = ContentService()
file_service = FileService()


@modules_bp.route('add', methods=['GET','POST'])
def module_add():
    if request.method == 'GET':
        playlists=content_service.get_playlists()
        return render_template('modules_add.html', playlists=playlists)
    
    elif request.method == 'POST':

        property_values=request.form

        is_active = False
        if property_values.get("is_active") == "True":
            is_active = True

        module = {
            "id": str(uuid.uuid4()),

            "created_by": "David",
            "date_created": datetime.utcnow(),
            "date_updated": datetime.utcnow(),
            "updated_by": "Julio",

            "description": property_values["description"],
            "is_active": is_active,
            "playlist_id": property_values["playlist_id"],
            "title": property_values["title"],
            "youtube_url": property_values["youtube_url"],
        }

        content_service.add_module(module=module)

        return redirect(url_for('modules.module_detail', module_id=module["id"]))

@modules_bp.route('detail/<module_id>')
def module_detail(module_id):
    module = content_service.get_module(module_id)
    playlist = content_service.get_playlist(module["playlist_id"])
    
    model = DetailModel(playlist=playlist, content=module)

    return render_template('modules_detail.html', model=model)

@modules_bp.route('edit/<module_id>', methods=['GET', 'POST'])
def module_edit(module_id):
    if request.method == 'POST':
        property_values=request.form

        module = content_service.get_module(module_id)

        # map new values to entity 
        is_active = False
        if property_values.get("is_active") == "True":
            is_active = True

        module["title"] = property_values["title"]
        module["date_updated"] = datetime.utcnow()
        module["description"] = property_values["description"]
        module["is_active"] = is_active
        module["playlist_id"] = property_values["playlist_id"]
        module["title"] = property_values["title"]
        module["updated_by"] = "Test user"

        content_service.update_module(module_id=module_id, module_to_update=module)

        return redirect(url_for('modules.module_detail', module_id=module["id"]))

    # render the edit form
    elif request.method == 'GET':
        module = content_service.get_module(module_id)
        playlists = content_service.get_playlists()
        model = EditModel(playlists=playlists, content=module)
    
        return render_template('modules_edit.html', model=model)
    
@modules_bp.route('file_upload/<module_id>', methods=['POST'])
def module_file_upload(module_id):
    
    # Check if the 'file' key is present in request.files
    if not request.files:
        print('No file in the request')
        raise Exception('No file in the request')
    
    file_info_items = []
    for file in request.files.getlist('file'):
        file_name = file.filename
        file_type = get_file_type(file_name)
        file_contents = file.read()
        
        blob_url = file_service.upload_to_blob(blob_name=file_name, content=file_contents, file_type=file_type)

        file_info_items.append(
            {
                "file_name": file_name, 
                "blob_url": blob_url,
                "file_type": file_type.value["display_name"]
            }
        )

    # add the data about the files to the module
    module = content_service.get_module(module_id)

    if module.get("attachments") == None:
        module["attachments"] = []
    
    for item in file_info_items:
        # get rid of any existing attachments with the same blob_url
        for existing_attachment in module["attachments"]:
            if existing_attachment["blob_url"] == item["blob_url"]:
                module["attachments"].remove(existing_attachment)
        
        module["attachments"].append(item)

    content_service.update_module(module_id=module_id, module_to_update=module)
    
    return redirect(request.referrer)

@modules_bp.route('attachment_delete/<module_id>/<blob_url>', methods=['POST'])
def module_attachment_delete(module_id, blob_url):
    # module = content_service.get_module(module_id)["module"]
    pass


def get_file_type(file_name):
    if file_name.endswith(".pdf"):
        return FileType.PDF
    elif file_name.endswith(".pptx"):
        return FileType.SLIDE
    elif file_name.endswith(".txt"):
        return FileType.TRANSCRIPT
    elif file_name.endswith(".mp4"):
        return FileType.VIDEO
    else:
        return FileType.OTHER