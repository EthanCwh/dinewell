import os
import secrets
from PIL import Image
from flask import escape, request, render_template, url_for, flash, redirect, session
from dinewell.forms import RegistrationForm, LoginForm, RestaurantRegistration, RestaurantLogin, MenuForm, StaffForm, ReviewForm, Review
from dinewell import app, db, bcrypt
from dinewell.models import User, Post, Restaurant, Menu, Staff
from flask_login import login_user, current_user, logout_user, login_required
    

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html", Title='Home')

@app.route('/userhome')
def user_home():
    return render_template("user_home.html", Title='User Home')

@app.route('/restauranthome')
def restaurant_home():
    return render_template("restaurant_home.html", Title='Restaurant Home')

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
        restaurant_user = Restaurant(email=form.email.data,  RestaurantName=form.RestaurantName.data, location=form.location.data, password=hashed_password)
        db.session.add(restaurant_user)
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


@app.route('/account')
@login_required
def account():
    return render_template("account.html", Title='Account')


@app.route("/menu/add", methods=['GET', 'POST'])
@login_required
def add_menu():
    form = MenuForm()
    if form.validate_on_submit():
        menu = Menu(name=form.name.data, owner_id=current_user.id)
        db.session.add(menu)
        db.session.commit()
        flash('Uploaded succesfully!', 'success')
    return render_template('restaurant_menu.html', title='Add Menu', form=form)

def save_staff_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/staff_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/staff/add", methods=['GET', 'POST'])
@login_required
def add_staff():
    form = StaffForm()
    if form.validate_on_submit():
        staff = Staff(name=form.name.data, owner_id=current_user.id)
        db.session.add(staff)
        db.session.commit()
        flash('Uploaded succesfully!', 'success')
        if form.picture.data:
            picture_file = save_staff_picture(form.picture.data)
    return render_template('restaurant_staff.html', title='Add Staff', form=form)

@app.route("/review", methods=['GET', 'POST'])
@login_required
def review():
    form = Review()
    if form.validate_on_submit():
        restaurant_id = Restaurant.query.filter_by(RestaurantName=form.restaurant_options.data.RestaurantName).first().id
        session['rid'] = restaurant_id 
        return redirect(url_for('new_review'))
    return render_template('review.html', title='Review', form=form)


@app.route("/review/new", methods=['GET', 'POST'])
@login_required
def new_review():
    form = ReviewForm()
    r_id = session["rid"]
    if form.validate_on_submit():
        review = Post(title=form.title.data, menu_options=form.menu_options.data.name, content_menu=form.content_menu.data, staff_options=form.staff_options.data.name, content_staff=form.content_staff.data, content_additional=form.content_additional.data, user_id=current_user.id)
        db.session.add(review)
        db.session.commit()
        flash('Submitted succesfully!', 'success')
    return render_template('new_review.html', title='New Review', form=form)
