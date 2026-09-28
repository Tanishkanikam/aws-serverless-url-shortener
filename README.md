# AWS Serverless URL Shortener & Analytics

A serverless URL shortening application built using AWS Lambda, API Gateway, DynamoDB, IAM, and CloudWatch.

The application accepts a long URL, generates a unique short code, stores the URL in DynamoDB, redirects users to the original URL, and tracks the number of clicks.

## Architecture

User → API Gateway → Lambda → DynamoDB

CloudWatch is used for monitoring and logs.

## AWS Services Used

### AWS Lambda
Python backend that handles URL creation, URL lookup, redirects, and click counting.

### Amazon API Gateway
Provides the HTTP API endpoints:

- POST /shorten
- GET /{shortCode}

### Amazon DynamoDB
Stores URL mappings.

Table name: URLMappings

Partition key: shortCode

Stored information:
- shortCode
- originalUrl
- clickCount

### Amazon CloudWatch
Used to monitor Lambda executions and application logs.

### AWS IAM
Provides permissions for Lambda to access DynamoDB.

## How It Works

### 1. Create a Short URL

The client sends a long URL to the POST /shorten endpoint.

Lambda generates a random 6-character short code and stores the URL in DynamoDB.

Example:

Long URL: https://www.google.com

Short code: ZVeSne

### 2. Use the Short URL

The user accesses the short URL through the GET /{shortCode} endpoint.

Lambda retrieves the original URL from DynamoDB and returns an HTTP 302 redirect.

### 3. Click Analytics

Every time a short URL is accessed, the clickCount value in DynamoDB is increased.

## Example DynamoDB Record

shortCode: ZVeSne

originalUrl: https://www.google.com

clickCount: 2

## Monitoring

CloudWatch logs record important application events such as:

- URL creation
- Short-code generation
- URL lookup
- Redirects
- Errors

## Security

The Lambda function uses an IAM execution role to access DynamoDB.

The project uses AWS permissions to control access between services.

## Key Concepts Demonstrated

- Serverless architecture
- AWS Lambda
- Amazon API Gateway
- Amazon DynamoDB
- AWS IAM
- Amazon CloudWatch
- REST APIs
- HTTP status codes
- JSON
- Application logging
- DynamoDB key-value storage

## Future Improvements

- Custom domain
- URL expiration
- Authentication
- Rate limiting
- Better URL validation
- Custom short codes
- Infrastructure as Code using Terraform or AWS SAM
- CI/CD deployment pipeline
- CloudWatch alarms

## Project Structure

aws-serverless-url-shortener/

- lambda_function.py
- README.md

## Author

Tanishka

Built as a cloud engineering project to demonstrate practical experience with AWS serverless services.
