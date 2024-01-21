from datetime import datetime
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
        module = content_service.add_module(module_properties=request.form)
        model = DetailModel(playlist=module["playlist"], content=module["module"])
        return redirect(url_for('modules.module_detail', module_id=model.content["id"]))

@modules_bp.route('detail/<module_id>')
def module_detail(module_id):
    module = content_service.get_module(module_id)
    
    model = DetailModel(playlist=module["playlist"], content=module["module"])
    
    return render_template('modules_detail.html', model=model)

@modules_bp.route('edit/<module_id>', methods=['GET', 'POST'])
def module_edit(module_id):
    if request.method == 'POST':
        new_values=request.form

        _, content_collection = content_service.get_collections()
        
        module = content_collection.find_one({"id": new_values["id"]})
        
        # map new values to entity 
        is_active = False
        if new_values.get("is_active") == "True":
            is_active = True

        module["title"] = new_values["title"]
        module["date_updated"] = datetime.utcnow()
        module["description"] = new_values["description"]
        module["is_active"] = is_active
        module["playlist_id"] = new_values["playlist_id"]
        module["title"] = new_values["title"]
        module["updated_by"] = "Test user"


        content_service.update_module(module_to_update=module)

        return redirect(url_for('modules.module_detail', module_id=module["id"]))

    # render the edit form
    elif request.method == 'GET':
        module = content_service.get_module(module_id)["module"]
        playlists = content_service.get_playlists()
        model = EditModel(playlists=playlists, content=module)
    
        return render_template('modules_edit.html', model=model)
    
@modules_bp.route('file_upload/<module_id>', methods=['POST'])
def module_file_upload(module_id):
    
    # Check if the 'file' key is present in request.files
    if 'file' not in request.files:
        print('No file in the request')
        raise Exception('No file in the request')
    
    file=request.files["file"]
    file_name = file.filename
    file_type = get_file_type(file_name)
    file_contents = file.read()

    blob_url = file_service.upload_to_blob(blob_name=file_name, content=file_contents, file_type=file_type)

    module = content_service.get_module(module_id)
    module[file_type.value["content_key"]] = blob_url

    print(f"Updating module: {module['module']['id']}")  

    content_service.update_whole_module(new_module=module)
    
    return redirect(url_for('modules.module_detail', module_id=module_id))

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