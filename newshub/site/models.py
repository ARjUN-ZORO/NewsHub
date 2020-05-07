from newshub import pos_db, login_manager
from datetime import datetime
from flask_login import UserMixin
from .settings import SECRET
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(pos_db.Model, UserMixin):
    __tablename__ = "user"
    id = pos_db.Column(pos_db.Integer, primary_key=True)
    email = pos_db.Column(pos_db.String(50), unique=True)
    username = pos_db.Column(pos_db.String(20))
    password = pos_db.Column(pos_db.String(255))
    dob = pos_db.Column(pos_db.Date())
    # phone = pos_db.Column(pos_db.Integer)
    address = pos_db.Column(pos_db.String(200))
    #j_date = pos_db.Column(pos_db.Date())
    # active = pos_db.Column(pos_db.Boolean(),nullable=False,server_default='0')

    # def __init__(self, email, username):
    #     self.email = email
    #     self.username = username

    # def serialize(self):
    #     return {"id": self.id,
    #             "email": self.email,
    #             "username": self.username}
