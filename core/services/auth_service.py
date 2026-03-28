import hashlib
from typing import Optional
from core.database.manager import DatabaseManager, GET_USER_ROLE


class AuthService:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def verify_login(self, username: str, plain_password: str) -> Optional[str]:
        hashed = hashlib.sha256(plain_password.encode()).hexdigest()
        row = self.db.fetchone(GET_USER_ROLE, (username, hashed))
        return row["role"] if row else None
