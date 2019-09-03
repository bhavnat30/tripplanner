import boto3
import time
# Create SQS client
#AWSAccessKeyId=AKIAJGSVG7ZZ4KNSUHFA
# AWSSecretKey=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
# Region: eu-west-1
# Default Format:JSON
sqs = boto3.client('sqs')
queue_url = 'https://sqs.eu-west-1.amazonaws.com/447123079606/City'
queue_list=sqs.list_queues()
ADMINS = frozenset([
	"ankitdongre96@gmail.com","bhavnat30@gmail.com"
	])
def checkAdm(x):
    flag=0
    for v in ADMINS:
            if x == v:
                print(x)
                flag=1
            if(flag==1):
                print("Admin Found")
                return 1
                break
            else:
                print("Not an admin")
                return 0
users=input("Enter your email-id\n")
if users in ADMINS:
                # Receive message from SQS queue
                    response = sqs.receive_message(
                        QueueUrl=queue_url,
                        AttributeNames=[
                            'SentTimestamp'
                        ],
                        MaxNumberOfMessages=1,
                        MessageAttributeNames=[
                            'All'
                        ],
                        VisibilityTimeout=0,
                        WaitTimeSeconds=0
                    )

                    if 'Messages' in response:
                       try:
                           for msg in response['Messages']:
                            # print('Got msg "{0}"'.format(msg['Body']))
                            print('got queue message')
                             # message = response['Messages'][0]
                            Attr = msg['MessageAttributes']
                            receipt_handle = msg['ReceiptHandle'] #Every time you receive a message from a queue, you receive a receipt handle for that message. This handle is associated with the action of receiving the message, not with the message itself. To delete the message or to change the message visibility, you must provide the receipt handle (not the message ID).
                                # Delete received message from queue will raise error if try to delete from empty queue
                            sqs.delete_message(
                            QueueUrl=queue_url,
                            ReceiptHandle=receipt_handle
                             )
                            # print('Received and deleted message: %s' % message['Body'])
                            # print(Attr['Title']['StringValue'])
                            # time.sleep(2)
                            print('MetaData: %s' % msg['MessageAttributes'])
                            time.sleep(2)
                            print('Received and deleted message: %s' % msg['Body'])
                            time.sleep(3)

                       except:
                               print("Sorry no messages for you", users)
                               pass
                               time.sleep(5)
                    else:
                        print('No messages in queue')
else:
        time.sleep(5)
