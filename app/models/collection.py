from app import db
from datetime import datetime


class Collection(db.Model):
    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    cover_image = db.Column(db.String(500), default="")
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    creator = db.relationship("User", backref="user_collections")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "cover_image": self.cover_image,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "archive_count": len(self.archive_items),
        }
