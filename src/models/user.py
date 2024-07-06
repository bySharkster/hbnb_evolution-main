from enum import auto
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.orm import Mapped
from src import db

"""
User related functionality
"""

class User(db.Model):
    
    __tablename__ = "users"

    id: Mapped[str] = Column(String(36), primary_key=True, nullable=False, unique=True, autoincrement=False, default=str(uuid.uuid4()))
    email: Mapped[str] = Column(String(120), unique=True, nullable=False)
    password: Mapped[str] = Column(String(128), nullable=False)
    first_name: Mapped[str] = Column(String(60), nullable=False)
    last_name: Mapped[str] = Column(String(60), nullable=False)
    is_admin: Mapped[bool] = Column(Boolean, default=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = Column(DateTime, onupdate=datetime.now, nullable=False)

    def __init__(self, email: str, first_name: str, last_name: str, **kw):
        """Initialize a User object"""
        super().__init__(**kw)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<User {self.id} ({self.email})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


    @staticmethod
    def get_all() -> list["User"]:
        """Get all users"""

        return User.query.all()
    
    @staticmethod
    def get(user_id: str) -> "User | None":
        """Get a user by ID"""

        return User.query.get(user_id)
    
    @staticmethod
    def create(user: dict) -> "User":
        """Create a new user"""

        users: list["User"] = User.get_all()

        for u in users:
            if u.email == user["email"]:
                raise ValueError("User already exists")

        new_user = User(**user)
        return new_user

    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        """Update an existing user"""

        user: User | None = User.get(user_id)

        if not user:
            return None

        if "email" in data:
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        return user

