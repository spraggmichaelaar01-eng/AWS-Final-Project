#!/usr/bin/python3
import json
import os
import boto3

# Use just the table name, not the full ARN
TABLE = "CS79C_TABLE"
REGION = os.environ.get("CS79C_REGION", "us-west-2")

print("Content-Type: application/json")
print("Cache-Control: no-store")
print()

try:
    if not TABLE:
        raise RuntimeError("CS79C_TABLE is not configured.")

    # Initialize boto3 DynamoDB resource (automatically uses EC2 Instance Profile credentials)
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    table = dynamodb.Table(TABLE)

    # Scan the table (boto3 automatically handles standard types without {"S": ...} wrappers)
    response = table.scan()
    items = response.get("Items", [])

    records = []
    for item in items:
        records.append({
            "MessageId": item.get("MessageId", ""),
            "Message": item.get("Message", ""),
            "Timestamp": item.get("Timestamp", ""),
        })

    records.sort(key=lambda item: item["Timestamp"], reverse=True)
    print(json.dumps(records))
except Exception as error:
    print(json.dumps([]))