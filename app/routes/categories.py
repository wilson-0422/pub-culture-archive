from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.services.category_service import CategoryService
from app.services.archive_service import ArchiveService

categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


@categories_bp.route("/")
def list_categories():
    tree = CategoryService.get_tree()
    all_categories = CategoryService.get_all()
    return render_template("categories/list.html", tree=tree, categories=all_categories)


@categories_bp.route("/<int:category_id>")
def detail(category_id):
    category = CategoryService.get_by_id(category_id)
    if not category:
        flash("分类不存在", "danger")
        return redirect(url_for("categories.list_categories"))

    page = request.args.get("page", 1, type=int)
    pagination = ArchiveService.get_all(page=page, per_page=12, category_id=category_id)
    return render_template(
        "categories/detail.html",
        category=category,
        archives=pagination.items,
        pagination=pagination,
    )


@categories_bp.route("/create", methods=["POST"])
@login_required
def create():
    data = {
        "name": request.form.get("name", "").strip(),
        "description": request.form.get("description", ""),
        "parent_id": request.form.get("parent_id", type=int),
    }
    if not data["name"]:
        flash("分类名称不能为空", "danger")
        return redirect(url_for("categories.list_categories"))
    CategoryService.create(data)
    flash("分类创建成功", "success")
    return redirect(url_for("categories.list_categories"))


@categories_bp.route("/<int:category_id>/delete", methods=["POST"])
@login_required
def delete(category_id):
    if CategoryService.delete(category_id):
        flash("分类已删除", "success")
    else:
        flash("分类不存在", "danger")
    return redirect(url_for("categories.list_categories"))
