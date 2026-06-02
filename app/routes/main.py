from flask import Blueprint, render_template
from flask_login import current_user
from app.services.archive_service import ArchiveService
from app.services.category_service import CategoryService
from app.services.collection_service import CollectionService

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    total_archives = ArchiveService.count_total()
    total_categories = CategoryService.count_total()
    total_collections = CollectionService.count_total()
    status_counts = ArchiveService.count_by_status()
    recent_archives = ArchiveService.get_all(page=1, per_page=6).items
    categories = CategoryService.get_all()

    return render_template(
        "index.html",
        total_archives=total_archives,
        total_categories=total_categories,
        total_collections=total_collections,
        status_counts=status_counts,
        recent_archives=recent_archives,
        categories=categories,
    )
