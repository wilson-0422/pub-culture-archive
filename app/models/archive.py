from app import db
from datetime import datetime


archive_collection = db.Table(
    "archive_collection",
    db.Column("archive_id", db.Integer, db.ForeignKey("archives.id"), primary_key=True),
    db.Column("collection_id", db.Integer, db.ForeignKey("collections.id"), primary_key=True),
)


class Archive(db.Model):
    __tablename__ = "archives"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    era = db.Column(db.String(100), default="")
    location = db.Column(db.String(200), default="")
    image_url = db.Column(db.String(500), default="")
    status = db.Column(db.String(20), default="draft")
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = db.relationship("Category", backref="archives")
    collections = db.relationship("Collection", secondary=archive_collection, backref="archive_items")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category_id": self.category_id,
            "era": self.era,
            "location": self.location,
            "image_url": self.image_url,
            "status": self.status,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
