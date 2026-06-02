from app import db
from app.models.archive import Archive


class ArchiveService:
    @staticmethod
    def get_all(page=1, per_page=10, category_id=None, status=None, keyword=None):
        query = Archive.query
        if category_id:
            query = query.filter_by(category_id=category_id)
        if status:
            query = query.filter_by(status=status)
        if keyword:
            search_filter = f"%{keyword}%"
            query = query.filter(
                db.or_(
                    Archive.title.like(search_filter),
                    Archive.description.like(search_filter),
                    Archive.era.like(search_filter),
                    Archive.location.like(search_filter),
                )
            )
        return query.order_by(Archive.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def get_by_id(archive_id):
        return db.session.get(Archive, archive_id)

    @staticmethod
    def create(data, user_id=None):
        archive = Archive(
            title=data.get("title", ""),
            description=data.get("description", ""),
            category_id=data.get("category_id"),
            era=data.get("era", ""),
            location=data.get("location", ""),
            image_url=data.get("image_url", ""),
            status=data.get("status", "draft"),
            created_by=user_id,
        )
        db.session.add(archive)
        db.session.commit()
        return archive

    @staticmethod
    def update(archive_id, data):
        archive = db.session.get(Archive, archive_id)
        if not archive:
            return None
        for key, value in data.items():
            if hasattr(archive, key) and key != "id":
                setattr(archive, key, value)
        db.session.commit()
        return archive

    @staticmethod
    def delete(archive_id):
        archive = db.session.get(Archive, archive_id)
        if not archive:
            return False
        db.session.delete(archive)
        db.session.commit()
        return True

    @staticmethod
    def search(keyword, page=1, per_page=10):
        search_filter = f"%{keyword}%"
        query = Archive.query.filter(
            db.or_(
                Archive.title.like(search_filter),
                Archive.description.like(search_filter),
                Archive.era.like(search_filter),
                Archive.location.like(search_filter),
            )
        )
        return query.order_by(Archive.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

    @staticmethod
    def count_by_status():
        from sqlalchemy import func
        results = (
            db.session.query(Archive.status, func.count(Archive.id))
            .group_by(Archive.status)
            .all()
        )
        return {status: count for status, count in results}

    @staticmethod
    def count_total():
        return Archive.query.count()
