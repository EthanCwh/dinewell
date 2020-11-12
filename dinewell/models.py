from dinewell import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(200), unique=True, nullable=True)
    password = db.Column(db.String(60),nullable=True)
    posts = db.relationship('Post', backref= 'author', lazy=True)

    def __repr__(self):
        return f'User("{self.username}", "{self.email}", "{self.image_file}")'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    RestaurantName = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    menu_options = db.Column(db.String(100), nullable=False)
    content_menu = db.Column(db.Text, nullable=False)
    staff_options = db.Column(db.String(100), nullable=False)
    content_staff = db.Column(db.Text, nullable=False)
    content_additional = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    staff = db.relationship('Comment', backref='comment_owner', lazy=True)

    def __repr__(self):
        return f'Post("{self.RestaurantName}", "{self.title}", "{self.date_posted}", "{self.menu_options}", "{self.content_menu}", "{self.staff_options}", "{self.content_staff}", "{self.content_additional}", "{self.user_id}")'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f'{self.name}'

@login_manager.user_loader
def load_user(restaurant_id):
    return Restaurant.query.get(int(restaurant_id))


class Restaurant(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), nullable=True, unique=True)
    RestaurantName = db.Column(db.String(100), nullable=True, unique=True)
    password = db.Column(db.String(60), nullable=True)
    location = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    menu = db.relationship('Menu', backref='menu_owner', lazy=True)
    staff = db.relationship('Staff', backref='staff_owner', lazy=True)

    def __repr__(self):
        return f'Restaurant("{self.RestaurantName}")'

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

    def __repr__(self):
        return f'{self.name}'

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True)
    image_file = db.Column(db.String(20), nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

    def __repr__(self):
        return f'{self.name}'

