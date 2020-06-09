import boto3
import json
import sys
import botocore

s3_client = boto3.client('s3')
response = s3_client.list_buckets()
buckets = [bucket['Name'] for bucket in response['Buckets']]

resource_statement = "arn:aws:s3:::{}/*"
resource_statement2 = "arn:aws:s3:::{}/*"

deny_unsecure = {
    "Effect": "Deny",
    "Principal": "*",
    "Action": "*",
    "Resource": "",
    "Condition": {
        "Bool": {
            "aws:SecureTransport": "false"
        }
    }
}

deny_unsecure2 = {
    "Effect": "Deny",
    "Principal": "*",
    "Action": "*",
    "Resource": "",
    "Condition": {
        "Bool": {
            "aws:SecureTransport": "false"
        }
    }
}

default_policy = {
    "Version": "2012-10-17",
    "Statement": [
    ]
}

for bucket in buckets:
    try:
        result = s3_client.get_bucket_policy(Bucket=bucket)
        policy = json.loads(result['Policy'])
    except botocore.exceptions.ClientError:
        policy = default_policy
        print(f'ADDING EMPTY BUCKET POLICY TO S3 BUCKET: {bucket}')
    statements = policy['Statement']
    deny_unsecure['Resource'] = resource_statement.format(bucket)
    if deny_unsecure not in statements:
        print(f'APPENDING DENY_UNSECURE STATEMENT TO S3 BUCKET: {bucket}')
        statements.append(deny_unsecure)
    bucket_policy = json.dumps(policy)
    s3_client.put_bucket_policy(Bucket=bucket, Policy=bucket_policy)
