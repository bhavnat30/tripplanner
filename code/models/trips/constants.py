import boto3
COLLECTION = "trips"
queue_url = 'https://sqs.eu-west-1.amazonaws.com/447123079606/City'
sqs = boto3.client('sqs')
