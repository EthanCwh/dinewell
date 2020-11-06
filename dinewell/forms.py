from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, ValidationError
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
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RestaurantRegistration(FlaskForm):
    RestaurantName = StringField('Restaurant Name', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators= [DataRequired(), Email()])
    location = StringField('Location', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class RestaurantLogin(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class MenuForm(FlaskForm):
    name = StringField('Food/Drink Name', validators=[DataRequired()])
    submit = SubmitField('Add')

class StaffForm(FlaskForm):
    name = StringField('Staff Name', validators=[DataRequired()])
    picture = FileField('Picture of Staff', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')

def choice_query_menu():
    r_id = session["rid"]
    return Menu.query.filter_by(owner_id=r_id)


def choice_query_staff():
    r_id = session["rid"]
    return Staff.query.filter_by(owner_id=r_id)

class ReviewForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    menu_options = QuerySelectField('What did you eat/drink?', query_factory=choice_query_menu, allow_blank=False, get_label='name')
    content_menu = TextAreaField('Comments about food/drink', validators=[DataRequired()])
    staff_options = QuerySelectField('Who served you?', query_factory=choice_query_staff, allow_blank=False, get_label='name')
    content_staff = TextAreaField('Comments about staff', validators=[DataRequired()])
    content_additional = TextAreaField('Additional comments', validators=[DataRequired()])
    submit = SubmitField('Submit')

def choice_query_restaurant():
    return Restaurant.query

class Review(FlaskForm):
    restaurant_options = QuerySelectField('Which restaurant did you go to?', query_factory=choice_query_restaurant, allow_blank=False, get_label='RestaurantName')
    submit = SubmitField('Confirm')
    