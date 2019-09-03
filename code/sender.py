import boto3

# Create SQS client
sqs = boto3.client('sqs')
ADMINS = frozenset([
	"ankitdongre96@gmail.com","bhavnat30@gmail.com"
	])
queue_url = 'https://sqs.eu-west-1.amazonaws.com/447123079606/City'

# Send message to SQS queue
response = sqs.send_message(
    QueueUrl=queue_url,
    DelaySeconds=5,
    MessageAttributes={
        'Title': {
            'DataType': 'String',
            'StringValue': 'The Whistler'
        }
    },
    MessageBody=(
        'Information about current NY Times fiction bestseller for '
        'week of 02/08/2019.'
    )
)

print(response['MessageId'])