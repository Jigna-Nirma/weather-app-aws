import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    city = event.get('queryStringParameters') or {}
    city = city.get('city', 'Banglore')

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('weather-history')

    response = table.query(
        KeyConditionExpression=Key('City').eq(city),
        ScanIndexForward=False,
        Limit=10
    )

    items = response.get('Items', [])

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(items)
    }

