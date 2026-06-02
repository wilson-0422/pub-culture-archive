from app import db
from app.models.collection import Collection


class CollectionService:
    @staticmethod
    def get_all(page=1, per_page=10):
        return Collection.query.order_by(Collection.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def get_by_id(collection_id):
        return db.session.get(Collection, collection_id)

    @staticmethod
    def create(data, user_id=None):
        collection = Collection(
            name=data.get("name", ""),
            description=data.get("description", ""),
            cover_image=data.get("cover_image", ""),
            created_by=user_id,
        )
        db.session.add(collection)
        db.session.commit()
        return collection

    @staticmethod
    def update(collection_id, data):
        collection = db.session.get(Collection, collection_id)
        if not collection:
            return None
        for key, value in data.items():
            if hasattr(collection, key) and key != "id":
                setattr(collection, key, value)
        db.session.commit()
        return collection

    @staticmethod
    def delete(collection_id):
        collection = db.session.get(Collection, collection_id)
        if not collection:
            return False
        db.session.delete(collection)
        db.session.commit()
        return True

    @staticmethod
    def add_archive(collection_id, archive_id):
        from app.models.archive import Archive
        collection = db.session.get(Collection, collection_id)
        archive = db.session.get(Archive, archive_id)
        if not collection or not archive:
            return False
        if archive not in collection.archive_items:
            collection.archive_items.append(archive)
            db.session.commit()
        return True

    @staticmethod
    def remove_archive(collection_id, archive_id):
        from app.models.archive import Archive
        collection = db.session.get(Collection, collection_id)
        archive = db.session.get(Archive, archive_id)
        if not collection or not archive:
            return False
        if archive in collection.archive_items:
            collection.archive_items.remove(archive)
            db.session.commit()
        return True

    @staticmethod
    def count_total():
        return Collection.query.count()
