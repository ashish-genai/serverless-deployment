import os
import boto3
import json
from botocore.exceptions import ClientError
import jwt
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
cognito = boto3.client('cognito-idp')
user_table = dynamodb.Table(os.environ['USERTABLE'])
USER_POOL_ID = os.environ['USER_POOL_ID']
CLIENT_ID = os.environ['CLIENT_ID']

def handler(event, context):
    try:
        if event['httpMethod'] == 'POST':
            body = json.loads(event['body'])
            action = body.get('action')
            
            if action == 'signup':
                return signup(body)
            elif action == 'login':
                return login(body)
            elif action == 'verify':
                return verify_token(event)
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'message': 'Invalid action'})
                }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': str(e)})
        }

def signup(body):
    try:
        response = cognito.sign_up(
            ClientId=CLIENT_ID,
            Username=body['username'],
            Password=body['password'],
            UserAttributes=[
                {'Name': 'email', 'Value': body['email']},
            ]
        )
        
        # Create user in DynamoDB
        user_table.put_item(
            Item={
                'id': response['UserSub'],
                'username': body['username'],
                'email': body['email'],
                'role': 'employee'  # Default role
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User created successfully'})
        }
    except ClientError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': str(e)})
        }

def login(body):
    try:
        response = cognito.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': body['username'],
                'PASSWORD': body['password']
            },
            ClientId=CLIENT_ID
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'token': response['AuthenticationResult']['IdToken'],
                'refresh_token': response['AuthenticationResult']['RefreshToken']
            })
        }
    except ClientError as e:
        return {
            'statusCode': 401,
            'body': json.dumps({'message': 'Invalid credentials'})
        }

def verify_token(event):
    try:
        token = event['headers']['Authorization'].split(' ')[1]
        # Verify token with Cognito
        response = cognito.get_user(
            AccessToken=token
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'valid': True, 'user': response['Username']})
        }
    except Exception as e:
        return {
            'statusCode': 401,
            'body': json.dumps({'valid': False, 'message': str(e)})
        }