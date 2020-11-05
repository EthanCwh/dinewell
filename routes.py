import secrets
import os
from PIL import Image
from flask import escape, request, render_template, url_for, flash, redirect
from dinewell.forms import RegistrationForm, LoginForm, RestaurantRegistration, RestaurantLogin, UpdateUserForm
from dinewell import app, db, bcrypt
from dinewell.models import User, Post, Restaurant
from flask_login import login_user, current_user, logout_user, login_required
    

posts = [
    {
        'author': 'Kamal',
        'title': 'Basket and Beyond',
        'content': 'First post content',
        'date_posted': '25 Novemeber 2010'
    },
    {
        'author': 'Rachel',
        'title': 'Basket and Beyond 2010',
        'content': 'Second post content',
        'date_posted': '25 December 2010'
    }
]


@app.route('/about')
def about():
    return render_template("about.html", posts=posts)

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", Title='Home', posts=posts)

@app.route('/userhome')
def user_home():
    return render_template("user_home.html", Title='User Home', posts=posts)

@app.route('/restauranthome')
def restaurant_home():
    return render_template("restaurant_home.html", Title='Restaurant Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user_home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect (url_for('user_home'))
        else:
            flash (f'wrong username & name, {form.email.data}!', "danger")
    return render_template("login.html", Title='Login', form=form )



@app.route('/register', methods=['GET','POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created', "success")
        return redirect(url_for("home"))
    return render_template("registration.html", Title='Registration', form=form)

@app.route('/restaurantregistration', methods=['GET', 'POST'])
def RRegistration():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RestaurantRegistration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Restaurant(email=form.email.data, location=form.location.data, password=hashed_password, RestaurantName=form.RestaurantName.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Your restaurant account has been created', "success")
        return redirect (url_for('home'))
    return render_template("restaurantregistration.html", Title='Registration', form=form)

@app.route('/restaurantlogin', methods=['GET', 'POST'])
def Rlogin():
    if current_user.is_authenticated:
        return redirect(url_for('restaurant_home'))
    form = RestaurantLogin()
    if form.validate_on_submit():
        user = Restaurant.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect (url_for('restaurant_home'))
        else:
            flash (f'wrong email & password!', "danger")
    return render_template("restaurantlogin.html", Title='Login', form=form )
        
@app.route('/logout')
def logout():
    logout_user()
    return redirect (url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    # added in to resize the image and make it standardize
    # have to pip install Pillow
    output_size= (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateUserForm()
    image_file = url_for('static', filename='profile_pics/'+ current_user.image_file)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", Title='Account', form=form, image_file=image_file)



