from flask import Blueprint, redirect, render_template, request, url_for
from content_service import ContentService
from modules.models.detail_model import DetailModel
from modules.models.edit_model import EditModel

modules_bp = Blueprint(
    "modules", __name__, template_folder="templates"
)

content_service = ContentService()

@modules_bp.route('/modules/<module_id>')
def module_detail(module_id):
    module = content_service.get_module(module_id)
    
    model = DetailModel(playlist=module["playlist"], content=module["module"])
    
    return render_template('detail.html', model=model)

@modules_bp.route('/modules/<module_id>/edit')
def module_edit(module_id):
    module = content_service.get_module(module_id)["module"]
    playlists = content_service.get_playlists()
    
    model = EditModel(playlists=playlists, content=module)
    
    return render_template('edit.html', model=model)

@modules_bp.route('/modules/update', methods=['POST'])
def module_update():
    print(request.form)
    
    content_service.update_module(new_values=request.form)
    return redirect(url_for('modules.module_detail', module_id=request.form["id"]))

