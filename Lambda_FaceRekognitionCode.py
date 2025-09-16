from __future__ import print_function

import boto3
import json
import urllib

print('Loading function...')

# AWS Clients
dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')
rekognition = boto3.client('rekognition')

# --------------- Helper Functions ------------------

def index_faces(bucket, key):
    """Detect and index faces from the uploaded image in Rekognition"""
    response = rekognition.index_faces(
        Image={"S3Object": {"Bucket": bucket, "Name": key}},
        CollectionId="criminal_collection"   # Our collection for criminal faces
    )
    return response

def update_index(tableName, faceId, fullName, crimeType="Unknown", status="Unknown"):
    """Store faceId + metadata into DynamoDB"""
    response = dynamodb.put_item(
        TableName=tableName,
        Item={
            'RekognitionId': {'S': faceId},
            'FullName': {'S': fullName},
            'CrimeType': {'S': crimeType},
            'WantedStatus': {'S': status}
        }
    )
    return response

# --------------- Main Handler ------------------

def lambda_handler(event, context):
    print("Event received:", event)

    # Get bucket name and file name from the S3 event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(f"Processing file: {key} from bucket: {bucket}")

    try:
        # Step 1: Detect & index face using Rekognition
        response = index_faces(bucket, key)

        # Step 2: Store details into DynamoDB
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            faceId = response['FaceRecords'][0]['Face']['FaceId']

            # Get metadata (fullname, crime, status) from S3 object
            ret = s3.head_object(Bucket=bucket, Key=key)
            personFullName = ret['Metadata'].get('fullname', 'Unknown')
            crimeType = ret['Metadata'].get('crime', 'Unknown')
            status = ret['Metadata'].get('status', 'Unknown')

            # Save to DynamoDB table "criminal_records"
            update_index('criminal_records', faceId, personFullName, crimeType, status)

            print(f"Face indexed successfully: {faceId} ({personFullName})")

        return response

    except Exception as e:
        print(f"Error processing object {key} from bucket {bucket}. Error: {str(e)}")
        raise e
