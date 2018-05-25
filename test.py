import boto3
import json
import os
from botocore.client import Config

def process_dropzone():
    s3 = boto3.resource('s3',
                        endpoint_url='http://localhost:9001',
                        aws_access_key_id='minio',
                        aws_secret_access_key='minio123',
                        config=Config(signature_version='s3v4'),
                        region_name='us-east-1')

    srcBucket = os.environ['SRC_BUCKET']
    destBucket = os.environ['DST_BUCKET']

    src = s3.Bucket(srcBucket)
    for obj in src.objects.all():
        file_content = obj.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        json_content['processed']= True
        s3.Object(destBucket, obj.key).put(Body=json.dumps(json_content, indent=4, sort_keys=True))


if __name__ == '__main__':
    process_dropzone()
