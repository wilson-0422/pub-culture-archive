from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.archive_service import ArchiveService
from app.services.category_service import CategoryService
from werkzeug.utils import secure_filename
import os

archives_bp = Blueprint("archives", __name__, url_prefix="/archives")


@archives_bp.route("/")
def list_archives():
    page = request.args.get("page", 1, type=int)
    keyword = request.args.get("keyword", "")
    category_id = request.args.get("category_id", type=int)
    status = request.args.get("status", "")

    if keyword:
        pagination = ArchiveService.search(keyword, page=page, per_page=12)
    else:
        pagination = ArchiveService.get_all(
            page=page, per_page=12, category_id=category_id, status=status
        )

    categories = CategoryService.get_all()
    return render_template(
        "archives/list.html",
        archives=pagination.items,
        pagination=pagination,
        categories=categories,
        keyword=keyword,
        current_category=category_id,
        current_status=status,
    )


@archives_bp.route("/<int:archive_id>")
def detail(archive_id):
    archive = ArchiveService.get_by_id(archive_id)
    if not archive:
        flash("档案不存在", "danger")
        return redirect(url_for("archives.list_archives"))
    return render_template("archives/detail.html", archive=archive)


@archives_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        data = {
            "title": request.form.get("title", "").strip(),
            "description": request.form.get("description", ""),
            "category_id": request.form.get("category_id", type=int),
            "era": request.form.get("era", "").strip(),
            "location": request.form.get("location", "").strip(),
            "status": request.form.get("status", "draft"),
        }

        image_file = request.files.get("image")
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            from flask import current_app
            upload_dir = current_app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_dir, exist_ok=True)
            filepath = os.path.join(upload_dir, filename)
            image_file.save(filepath)
            data["image_url"] = f"/static/images/{filename}"

        if not data["title"]:
            flash("标题不能为空", "danger")
            categories = CategoryService.get_all()
            return render_template("archives/create.html", categories=categories, data=data)

        archive = ArchiveService.create(data, user_id=current_user.id)
        flash("档案创建成功", "success")
        return redirect(url_for("archives.detail", archive_id=archive.id))

    categories = CategoryService.get_all()
    return render_template("archives/create.html", categories=categories, data={})


@archives_bp.route("/<int:archive_id>/edit", methods=["GET", "POST"])
@login_required
def edit(archive_id):
    archive = ArchiveService.get_by_id(archive_id)
    if not archive:
        flash("档案不存在", "danger")
        return redirect(url_for("archives.list_archives"))

    if request.method == "POST":
        data = {
            "title": request.form.get("title", "").strip(),
            "description": request.form.get("description", ""),
            "category_id": request.form.get("category_id", type=int),
            "era": request.form.get("era", "").strip(),
            "location": request.form.get("location", "").strip(),
            "status": request.form.get("status", "draft"),
        }

        image_file = request.files.get("image")
        if image_file and image_file.filename:
            filename = secure_filename(image_file.filename)
            from flask import current_app
            upload_dir = current_app.config["UPLOAD_FOLDER"]
            os.makedirs(upload_dir, exist_ok=True)
            filepath = os.path.join(upload_dir, filename)
            image_file.save(filepath)
            data["image_url"] = f"/static/images/{filename}"

        if not data["title"]:
            flash("标题不能为空", "danger")
            categories = CategoryService.get_all()
            return render_template("archives/edit.html", archive=archive, categories=categories)

        ArchiveService.update(archive_id, data)
        flash("档案更新成功", "success")
        return redirect(url_for("archives.detail", archive_id=archive_id))

    categories = CategoryService.get_all()
    return render_template("archives/edit.html", archive=archive, categories=categories)


@archives_bp.route("/<int:archive_id>/delete", methods=["POST"])
@login_required
def delete(archive_id):
    if ArchiveService.delete(archive_id):
        flash("档案已删除", "success")
    else:
        flash("档案不存在", "danger")
    return redirect(url_for("archives.list_archives"))
