from flask import Blueprint, redirect, render_template, request, url_for
from search.models.search_results_model import SearchResultsModel
from services.search_service import SearchService

search_bp = Blueprint(
    "search", __name__, 
    template_folder="templates", 
    static_folder="static"
)

search_service = SearchService()

@search_bp.route("/", methods=["POST"])
def search_results():
    search_term = request.form["search_term"]
    
    if search_term == "":
        return redirect(url_for("home"))
    
    search_results = search_service.search_content(search_term)
    
    search_results_model = SearchResultsModel(search_term, search_results)
    
    return render_template("search_index.html", model=search_results_model)