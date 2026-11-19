import json
import time
from datetime import datetime, timezone
from decimal import Decimal
import boto3

dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("CloudPulse-Telemetry")


def lambda_handler(event, context):
    """Consume telemetry payloads from SQS and persist them into DynamoDB."""
    processed_count = 0

    for record in event.get("Records", []):
        # Invalid JSON or missing InstanceID raises an exception so SQS retries and routes to DLQ
        payload = json.loads(record["body"])

        if "InstanceID" not in payload:
            raise ValueError("Missing required field: InstanceID")

        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        expire_at = int(time.time()) + (7 * 24 * 60 * 60)  # 7-day TTL

        item = {
            "InstanceID": str(payload["InstanceID"]),
            "Timestamp": str(payload.get("Timestamp", now_iso)),
            "CPUUtilization": Decimal(str(payload.get("CPUUtilization", 0))),
            "Status": str(payload.get("Status", "Ingested-via-SQS")),
            "Source": "SQS-Lambda-Pipeline",
            "ExpireAt": expire_at,
        }

        table.put_item(Item=item)
        processed_count += 1
        print(f"Stored telemetry for {item['InstanceID']} at {item['Timestamp']}")

    return {
        "statusCode": 200,
        "processed": processed_count,
    }
