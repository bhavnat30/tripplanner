from common.database import Database
from eventbrite import Eventbrite
from flask import Flask, redirect
import models.trips.constants as TripConstants
import uuid
import models.trips.errors as UserErrors
app = Flask(__name__)
class Trip(object):
	

	def __init__(self, source, destination, total_days, first_city, reservation, _id = None):
		self.source = source
		self.destination = destination
		self.total_days = total_days
		self.first_city = first_city
		self.reservation=reservation
		self._id = uuid.uuid4().hex if _id is None else _id
		# self.go_to_external_url

	def __repr__(self):
		return "Here is a summary of your Trip to: {}, Enjoy your stay!".format(self.destination)

	def save_to_mongo(self):
		Database.update(TripConstants.COLLECTION, {"_id": self._id}, self.json())

	def json(self):
		return {
			"source": self.source,
			"_id": self._id,
			"destination": self.destination,
			"total_days": self.total_days,
			"first_city": self.first_city,
			"reservation": self.reservation
		}

	@classmethod
	def get_by_id(cls, item_id):
		return cls(**Database.find_one(TripConstants.COLLECTION, {"_id": item_id}))

	@classmethod
	def get_by_trip_id(cls, _id):
		return [cls(**elem) for elem in Database.find(TripConstants.COLLECTION, {"_id": _id})]

	# def get_vacant_events(self):
	# 	return (self.total_events - self.events_booked)

	
	def delete(self):
		Database.remove(TripConstants.COLLECTION, {"_id": self._id})

	@classmethod
	def all(cls):
		return [cls(**elem) for elem in Database.find(TripConstants.COLLECTION,{})]

	