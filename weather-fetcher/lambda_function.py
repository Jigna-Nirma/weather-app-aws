import json
import urllib.request
import os
from datetime import datetime, timezone
import boto3

def lambda_handler(event, context):
    city = event.get('city', 'Pune')
    
    api_key = os.environ['OPENWEATHER_API_KEY']
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode())

    record = {
        "City": data["name"],
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "temp_c": str(data["main"]["temp"]),
        "feels_like": str(data["main"]["feels_like"]),
        "humidity": str(data["main"]["humidity"]),
        "description": data["weather"][0]["description"],
        "wind_speed": str(data["wind"]["speed"])
    }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('weather-history')
    table.put_item(Item=record)

    print("Saved to DynamoDB:", record)
    return {
        "statusCode": 200,
        "body": json.dumps(record)
    }
