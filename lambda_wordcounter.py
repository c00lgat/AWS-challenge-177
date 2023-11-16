import boto3

def lambda_handler(event, context):
    # Initialize Boto3 clients
    s3_client = boto3.client('s3')
    sns_client = boto3.client('sns')

    # SNS topic ARN
    sns_topic_arn = 'arn:aws:sns:us-west-2:384520732589:WordCounterInvocation'

    # Extract bucket name and file key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']

    try:
        # Get the file from S3
        file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
        
        # Read the file content
        file_content = file_obj['Body'].read().decode('utf-8')

        # Count the words
        word_count = len(file_content.split())

        # Prepare the message
        message = f"The word count in the {file_key} file is {word_count}."

        # Publish the message to the SNS topic
        sns_client.publish(TopicArn=sns_topic_arn, Message=message)

        # Return a simple success message (or log it)
        return 'Message sent to SNS'
    
    except Exception as e:
        print(e)
        return 'Error processing the file'
