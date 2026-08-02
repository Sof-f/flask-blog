from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app import login
from flask_login import UserMixin

@login.user_loader
def load_user(id: str):
    return db.session.get(User, int(id))


class User(db.Model, UserMixin):
    # id:int = db.Column(db.Integer, primary_key=True)
    # username:str = db.Column(db.String(64), index=True, unique=True)
    # email:str = db.Column(db.String(120), index=True, unique=True)
    # password_hash:str = db.Column(db.String(128))

    id: so.Mapped[int] = db.Column(db.Integer, primary_key=True)
    username: so.Mapped[str] = db.Column(db.String(64), index=True, unique=True)
    email: so.Mapped[str] = db.Column(db.String(120), index=True, unique=True)
    password_hash: so.Mapped[str] = db.Column(db.String(128))


    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str):
        return check_password_hash(self.password_hash, password)


    posts: so.WriteOnlyMapped["Post"] = so.relationship(back_populates="author")
    def __repr__(self):
        return f"User {self.username}"


class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))

    timestamp: so.Mapped[Optional[datetime]] = so.mapped_column( index=True, default=lambda: datetime.now(tz=timezone.utc))

    user_id: so.Mapped[int] = so.mapped_column(db.Integer, db.ForeignKey(User.id), index=True)

    author: so.Mapped[User] = so.relationship(back_populates="posts")

    def __repr__(self):
        return f"Post {self.body}"

