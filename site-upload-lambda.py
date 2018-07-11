import boto3
import zipfile
from io import BytesIO
from botocore.client import Config

def lambda_handler(event, context):
    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
    site_bucket = s3.Bucket('www.danielhklein.com')
    build_bucket = s3.Bucket('build.danielhklein.com')
    
    site_zip = BytesIO()
    build_bucket.download_fileobj('build.zip', site_zip)
    
    with zipfile.ZipFile(site_zip) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            site_bucket.upload_fileobj(obj, nm)
            site_bucket.Object(nm).Acl().put(ACL='public-read')
    
    return
