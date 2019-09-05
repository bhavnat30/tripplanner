from common.database import Database
from eventbrite import Eventbrite
from flask import Flask, redirect
import models.flights.constants_message as FC
import uuid
import models.flights.errors as UserErrors
app = Flask(__name__)
class Mesevent(object):
	eventbrite = Eventbrite('NL3IVYPNAYASG6QYJSMF')
	user_id = eventbrite.get_user()['id']
	print("user is::::")
	print("%s",user_id)
	events = eventbrite.event_search(**{'user.id': user_id})
	print("%s",events)
	@app.route("/https://www.eventbrite.com/")
	def go_to_external_url():
		print("redirecting to eventbrite...")


	def __init__(self, city, _id = None):
		self.city= venue
		self._id = uuid.uuid4().hex if _id is None else _id
		self.go_to_external_url

	def __repr__(self):
		return "<Your events in city: {}>".format(self.city)

	def save_to_mongo(self):
		Database.update(FC.COLLECTION, {"_id": self._id}, self.json())


	def json(self):
		return {
			"city": self.city,
			"_id": self._id,
		}

	@classmethod
	def get_by_id(cls, item_id):
		return cls(**Database.find_one(FC.COLLECTION, {"_id": item_id}))

	@classmethod
	def get_by_event_id(cls, city):
		return [cls(**elem) for elem in Database.find(FC.COLLECTION, {"city": city})]

	# def get_vacant_events(self):
	# 	return (self.total_events - self.events_booked)

	def get_price(self):
		return self.price

	def delete(self):
		Database.remove(FC.COLLECTION, {"_id": self._id})

	@classmethod
	def all(cls):
		return [cls(**elem) for elem in Database.find(FC.COLLECTION,{})]

	@staticmethod
	def is_event_full():
		raise UserErrors.FlightFull("Sorry! All the events are currently full")
