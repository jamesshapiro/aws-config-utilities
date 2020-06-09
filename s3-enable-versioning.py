import boto3
import json
import sys
import botocore

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
response = s3_client.list_buckets()
bucket_names = [bucket['Name'] for bucket in response['Buckets']]

for bucket_name in bucket_names:
    bucket = s3_resource.Bucket(bucket_name)
    versioning = s3_resource.BucketVersioning(bucket_name)
    if versioning.status == None or versioning.status == 'Suspended':
        print(f'Bucket {bucket_name} ::: Versioning Status: {versioning.status} ::: ENABLING VERSIONING')
        versioning.enable()
    else: 
        print(f'Bucket {bucket_name} ::: Versioning Status: {versioning.status}')

    

