from . import db
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime

# user UserMixin for methods that the Flask-Login expects user objects to have
# this means we don't have to implement the methods manually
# methods such as is_authenticated, get_id()
class User(UserMixin, db.Model):
    __tablename__="users"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True) # the email must be unique
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(1000), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # use back_populates to establish a bidirectional relationship between tables
    # also use cascade to update deletion automatically
    # when a user is deleted, all of their folders are also deleted
    folders = relationship("Folder", back_populates="user", cascade="all, delete")

class Folder(db.Model):
    __tablename__="folders"

    id = db.Column(db.Integer, primary_key=True)
    folder_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), index=True)
    
    user = relationship('User', back_populates="folders")
    cards = relationship('Card', back_populates="folder", cascade="all, delete")

class Card(db.Model):
    __tablename__="cards"
    
    id = db.Column(db.Integer, primary_key=True)
    # card's information
    card_question = db.Column(db.String(1000), nullable=False)
    card_answer = db.Column(db.String(1000), nullable=False)
    
    # checkpoint for reviewing
    first_reviewed = db.Column(db.Boolean, default=False)
    second_reviewed = db.Column(db.Boolean, default=False)
    last_reviewed = db.Column(db.Boolean, default=False)
    
    # connect to the folder (study decks)
    folder_id = db.Column(db.Integer, db.ForeignKey("folders.id", ondelete="CASCADE"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_reviewed_at = db.Column(db.DateTime)
    
    folder = relationship("Folder", back_populates="cards")
