from flask import Blueprint, jsonify, request
from app.services.archive_service import ArchiveService
from app.services.category_service import CategoryService

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/search")
def search():
    keyword = request.args.get("q", "")
    page = request.args.get("page", 1, type=int)
    if not keyword:
        return jsonify({"results": [], "total": 0, "page": page})
    pagination = ArchiveService.search(keyword, page=page, per_page=20)
    results = [a.to_dict() for a in pagination.items]
    return jsonify({
        "results": results,
        "total": pagination.total,
        "page": page,
        "pages": pagination.pages,
    })


@api_bp.route("/categories")
def list_categories():
    categories = CategoryService.get_all()
    return jsonify([c.to_dict() for c in categories])


@api_bp.route("/stats")
def stats():
    from app.services.archive_service import ArchiveService
    from app.services.collection_service import CollectionService
    return jsonify({
        "total_archives": ArchiveService.count_total(),
        "total_categories": CategoryService.count_total(),
        "total_collections": CollectionService.count_total(),
        "status_counts": ArchiveService.count_by_status(),
    })
