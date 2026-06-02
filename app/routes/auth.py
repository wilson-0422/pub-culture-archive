from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get("next")
            flash("登录成功", "success")
            return redirect(next_page or url_for("main.index"))
        flash("用户名或密码错误", "danger")
    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        display_name = request.form.get("display_name", "").strip()

        if not username or not password:
            flash("用户名和密码不能为空", "danger")
            return render_template("auth/register.html")

        if password != confirm:
            flash("两次输入的密码不一致", "danger")
            return render_template("auth/register.html")

        if User.query.filter_by(username=username).first():
            flash("用户名已存在", "danger")
            return render_template("auth/register.html")

        user = User(username=username, display_name=display_name or username, role="viewer")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("注册成功，请登录", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("已退出登录", "info")
    return redirect(url_for("main.index"))
