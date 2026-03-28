from core.database.manager import (
    DatabaseManager,
    Category,
    GET_ALL_CATEGORIES,
    GET_CATEGORY_BY_ID,
    INSERT_CATEGORY,
    UPDATE_CATEGORY,
    DELETE_CATEGORY,
    COUNT_CATEGORIES,
)


class CategoryService:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def get_all(self) -> list[Category]:
        rows = self.db.fetchall(GET_ALL_CATEGORIES)
        return [Category(id=r["id"], name=r["name"]) for r in rows]

    def get_by_id(self, cat_id: int) -> Category | None:
        row = self.db.fetchone(GET_CATEGORY_BY_ID, (cat_id,))
        return (
            Category(
                id=row["id"], name=row["name"], description=row["description"] or ""
            )
            if row
            else None
        )

    def add(self, name: str, description: str) -> bool:
        if not name.strip():
            raise ValueError("Category name cannot be empty.")
        return self.db.execute(INSERT_CATEGORY, (name.strip(), description))

    def update(self, cat_id: int, name: str, description: str) -> bool:
        if not name.strip():
            raise ValueError("Category name cannot be empty.")
        return self.db.execute(UPDATE_CATEGORY, (name.strip(), description, cat_id))

    def delete(self, cat_id: int) -> bool:
        return self.db.execute(DELETE_CATEGORY, (cat_id,))

    def count(self) -> int:
        return self.db.scalar(COUNT_CATEGORIES) or 0
