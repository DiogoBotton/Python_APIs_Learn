from fastapi import Depends
from sqlalchemy.orm import Session
from src.data.database import get_db, Base

from src.domains.user import User
from src.domains.enums.role_type import RoleType
from src.infrastructure.security.password import hash_password

class DbSeeder:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def clean_db(self):
        for table in reversed(Base.metadata.sorted_tables):
            self.db.execute(table.delete())
        self.db.commit()

    def seed_users(self):
        admins = [User("admin@email.com", hash_password("Admin@123"), "000", RoleType.Administrator)]

        self.db.add_all(admins)
        self.db.commit()