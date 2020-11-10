from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_googlemaps import GoogleMaps



app = Flask(__name__)
app.config['SECRET_KEY']='e53a8b19893a812ecd94740e483635b3'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///dwdb.db'
app.config['GOOGLEMAPS_KEY'] = "AIzaSyDcdcJEqg_5O9BKYDcPV1Kxv-7GBAVkCVE"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
GoogleMaps(app)
login_manager.login_view='login'

from dinewell import routes

