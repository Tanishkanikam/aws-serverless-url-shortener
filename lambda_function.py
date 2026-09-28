import json
import boto3
import random
import string
import logging

# CloudWatch logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("URLMappings")


def generate_code(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def lambda_handler(event, context):

    # Create short URL
    if event.get("routeKey") == "POST /shorten":

        body = json.loads(event.get("body", "{}"))
        original_url = body.get("url")

        logger.info(f"Creating short URL for: {original_url}")

        if not original_url:
            logger.warning("URL was not provided")

            return {
                "statusCode": 400,
                "body": json.dumps({
                    "error": "URL is required"
                })
            }

        short_code = generate_code()

        logger.info(f"Generated short code: {short_code}")

        table.put_item(
            Item={
                "shortCode": short_code,
                "originalUrl": original_url,
                "clickCount": 0
            }
        )

        logger.info(f"URL stored successfully: {short_code}")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "shortCode": short_code,
                "originalUrl": original_url
            })
        }

    # Redirect short URL
    if event.get("routeKey") == "GET /{shortCode}":

        short_code = event.get("pathParameters", {}).get("shortCode")

        logger.info(f"Looking up short code: {short_code}")

        response = table.get_item(
            Key={"shortCode": short_code}
        )

        item = response.get("Item")

        if not item:
            logger.warning(f"Short code not found: {short_code}")

            return {
                "statusCode": 404,
                "body": json.dumps({
                    "error": "Short URL not found"
                })
            }

        # Increase click count
        table.update_item(
            Key={"shortCode": short_code},
            UpdateExpression="SET clickCount = if_not_exists(clickCount, :zero) + :one",
            ExpressionAttributeValues={
                ":zero": 0,
                ":one": 1
            }
        )

        logger.info(f"Redirecting {short_code} to {item['originalUrl']}")

        return {
            "statusCode": 302,
            "headers": {
                "Location": item["originalUrl"]
            },
            "body": ""
        }

    logger.warning("Invalid request received")

    return {
        "statusCode": 400,
        "body": json.dumps({
            "error": "Invalid request"
        })
    }