from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    display_name = db.Column(db.String(120), default="")
    role = db.Column(db.String(20), default="viewer")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    archives = db.relationship("Archive", backref="author", lazy="dynamic")

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == "admin"
