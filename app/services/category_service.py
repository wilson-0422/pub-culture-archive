from app import db
from app.models.category import Category


class CategoryService:
    @staticmethod
    def get_all():
        return Category.query.order_by(Category.name).all()

    @staticmethod
    def get_by_id(category_id):
        return db.session.get(Category, category_id)

    @staticmethod
    def create(data):
        category = Category(
            name=data.get("name", ""),
            description=data.get("description", ""),
            parent_id=data.get("parent_id"),
        )
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def update(category_id, data):
        category = db.session.get(Category, category_id)
        if not category:
            return None
        for key, value in data.items():
            if hasattr(category, key) and key != "id":
                setattr(category, key, value)
        db.session.commit()
        return category

    @staticmethod
    def delete(category_id):
        category = db.session.get(Category, category_id)
        if not category:
            return False
        db.session.delete(category)
        db.session.commit()
        return True

    @staticmethod
    def get_tree():
        categories = Category.query.order_by(Category.name).all()
        tree = []
        lookup = {}
        for cat in categories:
            node = {"id": cat.id, "name": cat.name, "description": cat.description, "children": []}
            lookup[cat.id] = node
            if cat.parent_id and cat.parent_id in lookup:
                lookup[cat.parent_id]["children"].append(node)
            else:
                tree.append(node)
        return tree

    @staticmethod
    def count_total():
        return Category.query.count()
