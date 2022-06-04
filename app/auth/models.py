from flask_login import UserMixin
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

#for Post class
from slugify import slugify
from sqlalchemy.exc import IntegrityError

class User(db.Model, UserMixin):

    __tablename__ = 'blog_user' # <- es una palagra resevada de PosgrestSQL. Le da el nombre a la tabla

    id = db.Column(db.Integer, primary_key=True) # <- Con .Column, se define los campos de la DB.
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self): #<- Guarda los cambios en la DB
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
