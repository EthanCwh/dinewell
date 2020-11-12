import os
import secrets
from PIL import Image
from flask import escape, request, render_template, url_for, flash, redirect, session, abort, jsonify
from dinewell.forms import RegistrationForm, LoginForm, RestaurantRegistration, RestaurantLogin, UpdateUserForm, MenuForm, StaffForm, ReviewForm, Review, LocationForm, CommentForm
from dinewell import app, db, bcrypt
from dinewell.models import User, Post, Restaurant, Menu, Staff, Comment
from flask_login import login_user, current_user, logout_user, login_required
from geopy.geocoders import Nominatim
from sqlalchemy.sql import func
import requests

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()

    return render_template("home.html", Title='Home', reviews=posts)

@app.route('/userhome')
def user_home():
    posts = Post.query.all()
    return render_template("user_home.html", Title='User Home', reviews=posts)

@app.route('/restauranthome')
def restaurant_home():
    posts = Post.query.all()
    return render_template("restaurant_home.html", Title='Restaurant Home', reviews=posts)

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
        restaurant_user = Restaurant(email=form.email.data,  RestaurantName=form.RestaurantName.data, location=form.location.data,  address=form.address.data, password=hashed_password)
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
    return render_template("restaurantlogin.html", Title='Login', form=form)
        
@app.route('/logout')
def logout():
    logout_user()
    return redirect (url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size= (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", Title='Account', form=form)


@app.route("/menu/add", methods=['GET', 'POST'])
@login_required
def add_menu():
    form = MenuForm()
    if form.validate_on_submit():
        menu = Menu(name=form.name.data, owner_id=current_user.id)
        db.session.add(menu)
        db.session.commit()
        flash('Added succesfully!', 'success')
    return render_template('restaurant_menu.html', title='Add Menu', form=form)

def save_staff_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'sstaff_pics', picture_fn)
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
        flash('Added succesfully!', 'success')
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
        review = Post(RestaurantName=form.restaurant.data.RestaurantName, title=form.title.data, menu_options=form.menu_options.data.name, content_menu=form.content_menu.data, staff_options=form.staff_options.data.name, content_staff=form.content_staff.data, content_additional=form.content_additional.data, rating=form.rating.data, user_id=current_user.id)
        db.session.add(review)
        db.session.commit()
        flash('Submitted succesfully!', 'success')
        email = User.query.filter_by(id=current_user.id).first().email
        requests.post(
            "https://api.mailgun.net/v3/sandboxa8fff24026c2470aa1685cf71714e0ea.mailgun.org/messages",
		    auth=("api", app.config.get('MAILGUN_API')),
		    data={"from": "Mailgun Sandbox <postmaster@sandboxa8fff24026c2470aa1685cf71714e0ea.mailgun.org>",
			"to": email,
			"subject": "New review added to DineWell!",
			"text": "Thank you for adding a review!"})
        return redirect(url_for('user_home'))
    return render_template('new_review.html', title='New Review', form=form, legend='New Review')

@app.route("/review/<int:review_id>")
def review_id(review_id):
    review= Post.query.get_or_404(review_id)
    comment=Comment.query.get_or_404(review_id)
    return render_template('review_id.html', title=review.title, review=review, comment=comment)

@app.route("/review/<int:review_id>/comment", methods=['GET', 'POST'])
@login_required
def comment_review(review_id):
    review= Post.query.get_or_404(review_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comment=form.comment.data, owner_id=review_id)
        db.session.add(comment)
        db.session.commit()
        flash('Submitted succesfully!', 'success')
        return redirect(url_for('review_id', review_id=review.id))
    return render_template('comment_review.html', form=form)

@app.route("/review/<int:review_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review= Post.query.get_or_404(review_id)
    if review.author != current_user:
        abort(403)
    form = ReviewForm()
    if form.validate_on_submit():
        review.title = form.title.data
        review.menu_options = form.menu_options.data.name
        review.content_menu = form.content_menu.data
        review.staff_options = form.staff_options.data.name
        review.content_staff = form.content_staff.data
        review.content_additional = form.content_additional.data
        review.rating = form.rating.data
        db.session.commit()
        flash('Your review has been updated', 'success')
        return redirect(url_for('review_id', review_id=review.id))
    elif request.method == 'GET':
        form.title.data = review.title
        form.menu_options.data = review.menu_options
        form.content_menu.data = review.content_menu
        form.staff_options.data = review.staff_options
        form.content_staff.data = review.content_staff
        form.content_additional.data = review.content_additional
        form.rating.data = review.rating
    return render_template('new_review.html', title='Edit Review', form=form, legend='Edit Review')

@app.route("/review/<int:review_id>/delete", methods=['POST'])
@login_required
def delete_review(review_id):
    review= Post.query.get_or_404(review_id)
    if review.author != current_user:
        abort(403)
    db.session.delete(review)
    db.session.commit()
    flash('Your review has been deleted', 'success')
    return redirect(url_for('user_home'))

@app.route("/mapsearch", methods=['GET', 'POST'])
def map_search():
    form = LocationForm()
    if form.validate_on_submit():
        api = app.config.get("HERE_API")
        restaurant_address = Restaurant.query.filter_by(RestaurantName=form.RestaurantName.data).first().address
        geolocator = Nominatim(user_agent='myuseragent')
        coordinates = geolocator.geocode(restaurant_address)
        lat = coordinates.latitude
        lon = coordinates.longitude
        return render_template('map.html', lat=lat, lon=lon, api=api)
    return render_template('map_search.html', title='Search Restaurant', form=form)

@app.route("/chart")
def chart():
    return render_template('chart.html')


@app.route("/data")
def data():
    values = db.session.query(Post.rating).all()
    results = [results for results, in values]
    return jsonify({'results': results}) 

@app.route("/rating_average")
def rating_average():
    avg = db.session.query(Post.RestaurantName, db.func.avg(Post.rating).label("average_rating"))
    return render_template('rating_average.html', avg=avg)
