from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "请先登录后再访问此页面"


def create_app(config_class=None):
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
    )

    if config_class is None:
        from config import Config
        config_class = Config

    app.config.from_object(config_class)

    os.makedirs(app.config.get("UPLOAD_FOLDER", "/tmp/uploads"), exist_ok=True)
    instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance")
    os.makedirs(instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from app.routes.auth import auth_bp
    from app.routes.archives import archives_bp
    from app.routes.categories import categories_bp
    from app.routes.collections import collections_bp
    from app.routes.reports import reports_bp
    from app.routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(archives_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(collections_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(api_bp)

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    return app
