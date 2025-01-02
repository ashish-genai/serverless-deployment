import os
import boto3
from datetime import datetime

# Initialize DynamoDB resources
dynamodb = boto3.resource('dynamodb')

# Get table names from environment variables
USERS_TABLE = dynamodb.Table(os.environ['USERS_TABLE'])
ASSETS_TABLE = dynamodb.Table(os.environ['ASSETS_TABLE'])
ORDERS_TABLE = dynamodb.Table(os.environ['ORDERS_TABLE'])

class DatabaseManager:
    @staticmethod
    async def get_user(user_id: str):
        response = USERS_TABLE.get_item(Key={'id': user_id})
        return response.get('Item')

    @staticmethod
    async def create_user(user_data: dict):
        user_data['created_at'] = datetime.utcnow().isoformat()
        USERS_TABLE.put_item(Item=user_data)
        return user_data

    @staticmethod
    async def get_asset(asset_id: str):
        response = ASSETS_TABLE.get_item(Key={'id': asset_id})
        return response.get('Item')

    @staticmethod
    async def list_assets(limit: int = 100):
        response = ASSETS_TABLE.scan(Limit=limit)
        return response.get('Items', [])

    @staticmethod
    async def create_asset(asset_data: dict):
        asset_data['created_at'] = datetime.utcnow().isoformat()
        ASSETS_TABLE.put_item(Item=asset_data)
        return asset_data

    @staticmethod
    async def update_asset(asset_id: str, asset_data: dict):
        update_expression = "SET "
        expression_values = {}
        
        for key, value in asset_data.items():
            if key != 'id':
                update_expression += f"#{key} = :{key}, "
                expression_values[f":{key}"] = value
        
        update_expression = update_expression.rstrip(", ")
        
        response = ASSETS_TABLE.update_item(
            Key={'id': asset_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues="ALL_NEW"
        )
        return response.get('Attributes')

    @staticmethod
    async def create_order(order_data: dict):
        order_data['created_at'] = datetime.utcnow().isoformat()
        ORDERS_TABLE.put_item(Item=order_data)
        return order_data

    @staticmethod
    async def list_orders(user_id: str = None):
        if user_id:
            response = ORDERS_TABLE.query(
                IndexName='created_by-index',
                KeyConditionExpression='created_by = :user_id',
                ExpressionAttributeValues={':user_id': user_id}
            )
        else:
            response = ORDERS_TABLE.scan()
        return response.get('Items', [])