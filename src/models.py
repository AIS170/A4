from .database import db
from sqlalchemy.orm import relationship
# from flask_login import UserMixIn

class User(db.Model):
    id = db.Column(db.String(80), unique=True, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    #token = db.Column(db.String(150), unique=True, nullable=True)
    token_rel = relationship("Token", back_populates="user")

class Token(db.Model):
    id = db.Column(db.String(80), unique=True, primary_key=True)
    user_id = db.Column(db.String(80), db.ForeignKey('user.id'))
    user = relationship("User", back_populates="token_rel")

    # map 1:1 relationship