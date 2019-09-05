from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify
import uuid
from models.trips.trip import Trip
import models.trips.constants as TripConstants
from models.users.user import User
import models.flights.errors as UserErrors
import models.users.decorators as user_decorators
import requests
import json
import boto3
import time


sqs = boto3.client('sqs')
trip_blueprint = Blueprint('trips', __name__)

@trip_blueprint.route('/',methods=['GET'])
@user_decorators.requires_login
def index():
	trips = Trip.all()
	print(trips)

	# for t in trips:
	# 	output=[]
	# 	output.append({'source':t.source, 'destination':t.destination, 'total_days':t.total_days, 'first_city':t.first_city, 'reservation':t.reservation })
	# # return jsonify({'result':output})
	# print(output)
	return render_template('trips/trip_index.html', trips=trips)
	# return jsonify({'result':output})

@trip_blueprint.route('/1',methods=['GET'])
def jsonOutput():
	trips = Trip.all()
	print(trips)

	output=[]
	for t in trips:
		output.append({'source':t.source, 'destination':t.destination, 'total_days':t.total_days, 'first_city':t.first_city, 'reservation':t.reservation })
	# return jsonify({'result':output})
	print(output)
	# return render_template('trips/trip_index.html', trips=trips)
	return jsonify({'result':output})

@trip_blueprint.route('/city',methods=['GET'])
def jsonCity():
	trips = Trip.all()
	print(trips)

	output=[]
	for t in trips:
		output={'source':t.source, 'destination':t.destination, 'total_days':t.total_days, 'first_city':t.first_city, 'reservation':t.reservation }
	# return jsonify({'result':output})
	print(output)
	# return render_template('trips/trip_index.html', trips=trips)
	return jsonify({'result':output})


@trip_blueprint.route('/flight_view/<string:flight_id>')
def flight_page(_id):
	event = Flight.get_by_id(_id)
	return render_template("trips/flight.html", event = event)



@trip_blueprint.route('/add_', methods=['GET','POST'])
@user_decorators.requires_login
def trip_add():
	if request.method == 'POST':

		# event_name = request.form['event_name']
		# venue = request.form['venue']
		source = request.form['source']
		destination = request.form['destination']
		total_days = int(request.form['total_days'])
		first_city = request.form['first_city']
		reservation = request.form['reservation']
		#messaging code begins - sender code
		msg="Destination city sent for events is:"+destination
		res_msg = TripConstants.sqs.send_message(
				QueueUrl=TripConstants.queue_url, #Queue URL
				DelaySeconds=1,
				MessageAttributes={ #Metadata
						'Sender':{
							'DataType': 'String',
							'StringValue': destination
						}

				},
				MessageBody=( #Main Message
                      msg
				)
			)
		time.sleep(2)
		print(res_msg['MessageId'])
		# event_date = int(request.form['event_date'])
		
		# json_object=r.json()
		# print(json_object)

		Trip(source,destination,total_days,first_city,reservation).save_to_mongo()
		trip = {

			    "source": source,
				"destination": destination,
				"total_days": total_days,
				"first_city": first_city,
				"reservation": reservation
				# 	"total": total
				    }
		user = User.find_by_email(session['email'])
		user.trips = {uuid.uuid4().hex: trip}
		# 	# user.points_earned += (price/100)
		# print(user)
		trip_data=json.dumps(trip)
		#	 user.save_to_mongo()

		return redirect(url_for(".index"))
		return jsonify({'trips':trip})
	return render_template('trips/new_trip.html')

@trip_blueprint.route('/delete/<string:_id>')
@user_decorators.requires_login
def delete_trip(_id):
	Trip.get_by_id(_id).delete()
	return redirect(url_for('.index'))

@trip_blueprint.route('/edit/<string:_id>', methods=['PUT','POST'])
@user_decorators.requires_login
def edit_trip(_id):
	if request.method == 'PUT' or request.method == 'POST':
		source = request.form['source']
		destination = request.form['destination']
		total_days = int(request.form['total_days'])
		first_city = request.form['first_city']
		reservation = request.form['reservation']

		# event_date = int(request.form['event_date'])

		Trip(source,destination,total_days,first_city,reservation).save_to_mongo()
		trip = {

		    "source": source,
			"destination": destination,
			"total_days": total_days,
			"first_city": first_city,
			"reservation": reservation
			# 	"total": total
			    }
		user = User.find_by_email(session['email'])
		user.trips = {uuid.uuid4().hex: trip}
		
		return redirect(url_for(".index"))
	return render_template('trips/new_trip.html')
