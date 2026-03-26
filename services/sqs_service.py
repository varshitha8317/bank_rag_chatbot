import boto3

sqs = boto3.client('sqs', region_name='ap-south-1')

QUEUE_URL = "https://sqs.ap-south-1.amazonaws.com/176773471468/bank-queue"

def send_to_queue(message):
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=message
    )