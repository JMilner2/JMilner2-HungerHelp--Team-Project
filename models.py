"""
Author: Shaikha Almajed + Josh + Andrew + Vilius
Description: This code defines the database models for the user and post entities.
It also includes a function to initialize the database.
"""
from datetime import datetime
from app import db, app
import bcrypt
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    # User authentication information.
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.VARBINARY(100), nullable=False)
    # User information
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    notifications = db.Column(db.Boolean, nullable=False)
    # logging the date and time of all user registration
    registered_on = db.Column(db.DateTime, nullable=False)
    # logging the date and time of a user’s current login.
    current_login = db.Column(db.DateTime, nullable=True)
    # logging the date and time of a user’s previous login
    last_login = db.Column(db.DateTime, nullable=True)
    # logging in to be the role of user
    role = db.Column(db.String(20), nullable=False, default='user')

    def __init__(self, email, firstname, lastname, phone, password, notifications, role):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.phone = phone
        #hashing a password and using salt for more protection
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.notifications = notifications
        self.registered_on = datetime.now()
        self.current_login = None
        self.last_login = None
        self.role = role


class Post(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    recipe = db.Column(db.String(10000), nullable=False)
    ingredients = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable=True)

    def __init__(self, user_id, title, recipe, ingredients, image, price):
        self.user_id = user_id
        self.title = title
        self.recipe = recipe
        self.ingredients = ingredients
        self.image = image
        self.price = price
        self.views = 0


def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(email='admin@email.com',
                     password='Admin1!',
                     firstname='Team6',
                     lastname='Bob',
                     phone='0234-456-2333',
                     role='admin',
                     notifications=False)

        db.session.add(admin)
        db.session.commit()
