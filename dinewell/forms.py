from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, ValidationError, SelectField
from wtforms.validators import Length, DataRequired, Email, EqualTo
from dinewell.models import User, Post, Restaurant, Menu, Staff
from wtforms_sqlalchemy.fields import QuerySelectField
from flask import session

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=2, max=20), DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already taken')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RestaurantRegistration(FlaskForm):
    RestaurantName = StringField('Restaurant Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators= [DataRequired(), Email()])
    location = StringField('Location', validators = [DataRequired()])
    address = StringField('Address (optional)')
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_restaurantname(self, RestaurantName):
        restaurant = Restaurant.query.filter_by(RestaurantName=RestaurantName.data).first()
        if restaurant:
            raise ValidationError('Restaurant name already taken')

    def validate_email(self, email):
        email = Restaurant.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email already taken')

class RestaurantLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class UpdateUserForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=2, max=20), DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('Email already taken')

class MenuForm(FlaskForm):
    name = StringField('Food/Drink Name', validators=[DataRequired()])
    submit = SubmitField('Add')

class StaffForm(FlaskForm):
    name = StringField('Staff Name', validators=[DataRequired()])
    picture = FileField('Picture of Staff', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')

def choice_query_restaurant():
    r_id = session["rid"]
    return Restaurant.query.filter_by(id=r_id)

def choice_query_menu():
    r_id = session["rid"]
    return Menu.query.filter_by(owner_id=r_id)


def choice_query_staff():
    r_id = session["rid"]
    return Staff.query.filter_by(owner_id=r_id)

class ReviewForm(FlaskForm):
    restaurant = QuerySelectField('Restaurant:', query_factory=choice_query_restaurant, allow_blank=False, get_label='RestaurantName')
    title = StringField('Title', validators=[DataRequired()])
    menu_options = QuerySelectField('What did you eat/drink?', query_factory=choice_query_menu, allow_blank=False, get_label='name')
    content_menu = TextAreaField('Comments about food/drink', validators=[DataRequired()])
    staff_options = QuerySelectField('Who served you?', query_factory=choice_query_staff, allow_blank=False, get_label='name')
    content_staff = TextAreaField('Comments about staff', validators=[DataRequired()])
    content_additional = TextAreaField('Additional comments', validators=[DataRequired()])
    rating = SelectField('Rating', choices=[(5), (4), (3), (2), (1)])
    submit = SubmitField('Submit')

def choice_query_restaurant():
    return Restaurant.query

class Review(FlaskForm):
    restaurant_options = QuerySelectField('Which restaurant did you go to?', query_factory=choice_query_restaurant, allow_blank=False, get_label='RestaurantName')
    submit = SubmitField('Confirm')

class LocationForm(FlaskForm):
    RestaurantName = StringField('Restaurant Name', validators=[DataRequired()])
    submit = SubmitField('Search')

def choice_query_restaurant():
    r_id = session["rid"]
    return Restaurant.query.filter_by(id=r_id)

class CommentForm(FlaskForm):
    RestaurantName = StringField('Restaurant Name', validators=[DataRequired()])
    comment = TextAreaField('Comment:', validators=[DataRequired()])
    submit = SubmitField('Submit')
    