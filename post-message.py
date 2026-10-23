#!/usr/bin/python3
import html
import os
import sys
import uuid
import boto3
from datetime import datetime, timezone
from urllib.parse import parse_qs

# Use just the table name, not the full ARN
TABLE = "CS79C_TABLE"
REGION = os.environ.get("CS79C_REGION", "us-west-2")
MAX_LENGTH = 1000

print("Content-Type: text/html")
print()

try:
    length = int(os.environ.get("CONTENT_LENGTH", "0"))
    form = parse_qs(sys.stdin.read(length), keep_blank_values=True)
    message = form.get("message", [""])[0].strip()

    if not TABLE:
        raise RuntimeError("CS79C_TABLE is not configured.")
    if not message:
        raise ValueError("Message cannot be empty.")
    if len(message) > MAX_LENGTH:
        raise ValueError(f"Message cannot exceed {MAX_LENGTH} characters.")

    # Initialize boto3 DynamoDB resource (automatically uses EC2 Instance Profile credentials)
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    table = dynamodb.Table(TABLE)

    # Use standard python types with boto3 high-level resource
    table.put_item(
        Item={
            "MessageId": str(uuid.uuid4()),
            "Message": message,
            "Timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )

    print("<meta http-equiv='refresh' content='0;url=/'>")
    print("<p>Message posted. <a href='/'>Return to the board</a>.</p>")
except Exception as error:
    print("<h1>Unable to post message</h1>")
    print(f"<p>{html.escape(str(error))}</p>")
    print("<p><a href='/'>Return to the board</a>.</p>")