import json
import os

import boto3
from botocore.client import Config
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    process_dropzone()
    return 'Hello World2!'


if __name__ == '__main__':
    if os.environ.get('FLASK_DEBUG', False):
        app.run(host='0.0.0.0', port=8080, debug=True)
    else:
        app.run(host='0.0.0.0', port=80, debug=True)


def new_s3():
    return boto3.resource('s3',
                          endpoint_url='http://minio1:9000',
                          aws_access_key_id='minio',
                          aws_secret_access_key='minio123',
                          config=Config(signature_version='s3v4'),
                          region_name='us-east-1')


def process_dropzone():
    s3 = new_s3()
    srcBucket = os.environ['SRC_BUCKET']
    destBucket = os.environ['DEST_BUCKET']

    src = s3.Bucket(srcBucket)
    for obj in src.objects.all():
        file_content = obj.get()['Body'].read().decode('utf-8')
        json_content = json.loads(file_content)
        json_content['processed'] = True
        s3.Object(destBucket, obj.key).put(Body=json.dumps(json_content, indent=4, sort_keys=True))


# def setup_buckets():
#     s3 = new_s3()
#     src_bucket = os.environ['SRC_BUCKET']
#     dest_bucket = os.environ['DEST_BUCKET']
#
#     if not (s3.Bucket(src_bucket) in s3.buckets.all()):
#         s3.create_bucket(Bucket=src_bucket)
#     if not (s3.Bucket(dest_bucket) in s3.buckets.all()):
#         s3.create_bucket(Bucket=dest_bucket)
