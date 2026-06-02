from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.collection_service import CollectionService

collections_bp = Blueprint("collections", __name__, url_prefix="/collections")


@collections_bp.route("/")
def list_collections():
    page = request.args.get("page", 1, type=int)
    pagination = CollectionService.get_all(page=page, per_page=10)
    return render_template(
        "collections/list.html",
        collections=pagination.items,
        pagination=pagination,
    )


@collections_bp.route("/<int:collection_id>")
def detail(collection_id):
    collection = CollectionService.get_by_id(collection_id)
    if not collection:
        flash("合集不存在", "danger")
        return redirect(url_for("collections.list_collections"))
    return render_template("collections/detail.html", collection=collection)


@collections_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        data = {
            "name": request.form.get("name", "").strip(),
            "description": request.form.get("description", ""),
        }
        if not data["name"]:
            flash("合集名称不能为空", "danger")
            return render_template("collections/create.html", data=data)
        CollectionService.create(data, user_id=current_user.id)
        flash("合集创建成功", "success")
        return redirect(url_for("collections.list_collections"))
    return render_template("collections/create.html", data={})


@collections_bp.route("/<int:collection_id>/edit", methods=["GET", "POST"])
@login_required
def edit(collection_id):
    collection = CollectionService.get_by_id(collection_id)
    if not collection:
        flash("合集不存在", "danger")
        return redirect(url_for("collections.list_collections"))

    if request.method == "POST":
        data = {
            "name": request.form.get("name", "").strip(),
            "description": request.form.get("description", ""),
        }
        if not data["name"]:
            flash("合集名称不能为空", "danger")
            return render_template("collections/edit.html", collection=collection)
        CollectionService.update(collection_id, data)
        flash("合集更新成功", "success")
        return redirect(url_for("collections.detail", collection_id=collection_id))

    return render_template("collections/edit.html", collection=collection)


@collections_bp.route("/<int:collection_id>/delete", methods=["POST"])
@login_required
def delete(collection_id):
    if CollectionService.delete(collection_id):
        flash("合集已删除", "success")
    else:
        flash("合集不存在", "danger")
    return redirect(url_for("collections.list_collections"))


@collections_bp.route("/<int:collection_id>/add_archive", methods=["POST"])
@login_required
def add_archive(collection_id):
    archive_id = request.form.get("archive_id", type=int)
    if CollectionService.add_archive(collection_id, archive_id):
        flash("档案已添加到合集", "success")
    else:
        flash("添加失败，档案或合集不存在", "danger")
    return redirect(url_for("collections.detail", collection_id=collection_id))


@collections_bp.route("/<int:collection_id>/remove_archive/<int:archive_id>", methods=["POST"])
@login_required
def remove_archive(collection_id, archive_id):
    if CollectionService.remove_archive(collection_id, archive_id):
        flash("档案已从合集中移除", "success")
    else:
        flash("移除失败", "danger")
    return redirect(url_for("collections.detail", collection_id=collection_id))
