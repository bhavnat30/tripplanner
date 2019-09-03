from flask import Flask, render_template, request, session
from common.database import Database

from models.users.user import User
# from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
# from flask_dance.contrib.github import make_github_blueprint, github


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "123"
#
# twitter_blueprint = make_twitter_blueprint(api_key='', api_secret='')
# github_blueprint = make_github_blueprint(client_id='', client_secret='')
@app.before_first_request
def init_db():
	Database.initialize()

@app.route('/')
def home():
	return render_template("home.html")


from models.users.views import user_blueprint
from models.hotels.views import hotel_blueprint
from models.flights.views import flight_blueprint
from models.trips.views import trip_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(hotel_blueprint, url_prefix="/hotels")
app.register_blueprint(flight_blueprint, url_prefix="/events")
app.register_blueprint(trip_blueprint, url_prefix="/trips")
