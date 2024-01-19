from flask import Blueprint, redirect, render_template, request, url_for
from services.content_service import ContentService
from modules.models.detail_model import DetailModel
from modules.models.edit_model import EditModel

modules_bp = Blueprint(
    "modules", __name__, 
    template_folder="templates",
    static_folder="static",
)

content_service = ContentService()

@modules_bp.route('add', methods=['GET','POST'])
def module_add():
    if request.method == 'GET':
        playlists=content_service.get_playlists()
        return render_template('add.html', playlists=playlists)
    
    elif request.method == 'POST':
        module = content_service.add_module(new_values=request.form)
        model = DetailModel(playlist=module["playlist"], content=module["module"])
        return redirect(url_for('modules.module_detail', module_id=model.content["id"]))

@modules_bp.route('detail/<module_id>')
def module_detail(module_id):
    module = content_service.get_module(module_id)
    
    model = DetailModel(playlist=module["playlist"], content=module["module"])
    
    return render_template('detail.html', model=model)

@modules_bp.route('edit/<module_id>', methods=['GET', 'POST'])
def module_edit(module_id):
    # update the module and redirect to the detail page
    if request.method == 'POST':
        content_service.update_module(new_values=request.form)
        return redirect(url_for('modules.module_detail', module_id=request.form["id"]))

    # render the edit form
    elif request.method == 'GET':
        module = content_service.get_module(module_id)["module"]
        playlists = content_service.get_playlists()
        model = EditModel(playlists=playlists, content=module)
    
        return render_template('edit.html', model=model)