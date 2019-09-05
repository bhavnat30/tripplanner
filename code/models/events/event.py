from common.database import Database
from eventbrite import Eventbrite
from flask import Flask, redirect
import models.events.constants as FlightConstants
import uuid
import models.events.errors as UserErrors
app = Flask(__name__)
class Flight(object):
	eventbrite = Eventbrite('****')
	user_id = eventbrite.get_user()['id']
	print("user is::::")
	print("%s",user_id)
	events = eventbrite.event_search(**{'user.id': user_id})
	print("%s",events)
	@app.route("/https://www.eventbrite.com/")
	def go_to_external_url():
		print("redirecting to eventbrite...")


	def __init__(self, event_name,venue,event_date, _id = None):
		self.event_name = event_name
		self.event_date = event_date
		self.venue= venue
		self._id = uuid.uuid4().hex if _id is None else _id
		self.go_to_external_url

	def __repr__(self):
		return "<Your events: {}>".format(self.event_name)

	def save_to_mongo(self):
		Database.update(EventConstants.COLLECTION, {"_id": self._id}, self.json())

	
	def json(self):
		return {
			"event_name": self.event_name,
			"_id": self._id,
			"event_date": self.event_date,
			"venue": self.venue,
		}

	@classmethod
	def get_by_id(cls, item_id):
		return cls(**Database.find_one(EventConstants.COLLECTION, {"_id": item_id}))

	@classmethod
	def get_by_event_id(cls, event_name):
		return [cls(**elem) for elem in Database.find(EventConstants.COLLECTION, {"event_name": event_name})]

	# def get_vacant_events(self):
	# 	return (self.total_events - self.events_booked)

	def get_price(self):
		return self.price

	def delete(self):
		Database.remove(EventConstants.COLLECTION, {"_id": self._id})

	@classmethod
	def all(cls):
		return [cls(**elem) for elem in Database.find(EventConstants.COLLECTION,{})]

	@staticmethod
	def is_event_full():
		raise UserErrors.EventFull("Sorry! All the events are currently full")
