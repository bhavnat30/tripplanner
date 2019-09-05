from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify
import uuid

from models.events.event import Event
from models.events.mesevent import Mesevent
from models.users.user import User
from eventbrite import Eventbrite
import requests
import models.trips.constants as TripConstants
import models.events.constants as EventConstants
import models.events.errors as UserErrors
import models.users.decorators as user_decorators

event_blueprint = Blueprint('events', __name__)
city=""
@flight_blueprint.route('/')
@user_decorators.requires_login
def index():
	events = Event.all()
	#Listening for message
	try:
							response = TripConstants.sqs.receive_message(
										QueueUrl=TripConstants.queue_url, #queue url for identiying queue
										AttributeNames=[	#Metadata
											'SentTimestamp'
										],
										MaxNumberOfMessages=1,
										MessageAttributeNames=[
											'All'
										],
										VisibilityTimeout=0,
										WaitTimeSeconds=0
										)
							if 'Messages' in response: #Checking for Messages
										for msg in response['Messages']:
											# print('Got msg "{0}"'.format(msg['Body']))
												print('got queue message')
							else:
												print('No messages in queue')


							print("Try First")
							print(response['Messages'][0])
							message = response['Messages'][0] # Storing 1st message from response in message
							print("Try Second")
							Attr=message['MessageAttributes'] # Retrieving metadata from message
							print('before Handle')
							receipt_handle = message['ReceiptHandle'] #Receit Handle is generated on receipt of program and is needed for deleting
							print('before Delete')
							# Delete received message from queue will raise error if try to delete from empty queue
							TripConstants.sqs.delete_message(	#Deleting Messages
													QueueUrl=TripConstants.queue_url,
													ReceiptHandle=receipt_handle
												)
							#print('Received and deleted message: %s' % message['Body'])
							print (Attr['Sender']['StringValue'])
							global city
							city = message['MessageAttributes']['Sender']['StringValue']
							if city is None:
								# Mesevent.city = city
								print("no city value received")
								# Mesevent.save_to_mongo()

							# time.sleep(1)
							print('MetaData: %s' % message['MessageAttributes'])


							print('Received and deleted message: %s' % message['Body']) #Printing Message
							time.sleep(5)

							print("before saving to db")
	except:
							print("Sorry no messages for you") #No message Found



	return render_template('flights/flight_index.html', events=events)

@flight_blueprint.route('/events')
def events():
	# eventbrite = Eventbrite('NL3IVYPNAYASG6QYJSMF')
	val=[]
	date=[]
	venue=[]
	# city_temp= Mesevent.all()
	#call third party api using value from message should be present in the try catch block to handle delays
	print("$$$$${}".format(city))
	r= requests.get('https://www.eventbriteapi.com/v3/events/search/?location.address='+city+'&location.within=10km&expand=venue&token=NL3IVYPNAYASG6QYJSMF')
	json_object=r.json()

	if json_object is not None:
		even_k=json_object['events']
		print(len(even_k))

		for i in range(len(even_k)):
			val.append(even_k[i]['name']['text'])
			date.append(even_k[i]['start']['local'])
			venue.append(even_k[i]['venue']['address']['localized_address_display'])
		print(val)
		print(date)
		print(venue)

		return render_template("flight_book.html", event_val= val, date=date,venue=venue)
	else:
			return render_template("flight_exception.html")


							 #Exit loop
	# n= requests.get('https://www.eventbriteapi.com/v3/users/me')
	# https://www.eventbriteapi.com/v3/users/me/?token=NL3IVYPNAYASG6QYJSMF




@flight_blueprint.route('/1',methods=['GET'])
def jsonOutput():
	events = Event.all()
	print(events)

	output=[]
	for e in events:
		output.append({'event_name':e.event_name, 'event_date':e.event_date, 'venue':e.venue})
	
	print(output)
	
	return jsonify({'events':output})

@flight_blueprint.route('/city',methods=['GET'])
def jsonCity():

	# return render_template('trips/trip_index.html', trips=trips)
	return jsonify({'city':city})


@flight_blueprint.route('/flight_view/<string:flight_id>')
def flight_page(_id):
	event = Event.get_by_id(_id)
	return render_template("events/flight.html", event = event)


@flight_blueprint.route('/add_', methods=['GET', 'POST'])
@user_decorators.requires_login
def flight_add():
	if request.method == 'POST':
		event_name = request.form['event_name']
		venue = request.form['venue']
		event_date = int(request.form['event_date'])

		Event(event_name, event_date, venue).save_to_mongo()
		return redirect(url_for(".index"))
	return render_template('flights/new_flight.html')

@flight_blueprint.route('/delete/<string:_id>')
@user_decorators.requires_login
def delete_flight(_id):
	Event.get_by_id(_id).delete()
	return redirect(url_for('.index'))

@flight_blueprint.route('/booking_event/<string:event_name>/<string:event_date>/<string:venue>/', methods=['GET', 'POST'])
def flight_book(event_name,event_date,venue):
	 
	if request.method == 'POST':
		event_name = event_name
		event_date = event_date
		venue=venue
		
	order = {
	    "event_name": event_name,
		"event_date": event_date,
		"venue": venue
		
		    }
	user = User.find_by_email(session['email'])
	user.orders = {uuid.uuid4().hex : order}
		
	print(user)
	Event(event_name,event_date,venue).save_to_mongo()
	
	events = Event.all()
	return render_template('flights/flight_index.html', events=events)
