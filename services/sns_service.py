import boto3

sns = boto3.client('sns', region_name='ap-south-1')

TOPIC_ARN = "arn:aws:sns:ap-south-1:176773471468:bank-alerts"

def send_alert(message):
    sns.publish(
        TopicArn=TOPIC_ARN,
        Message=message,
        Subject="🏦 Bank Alert"
    )