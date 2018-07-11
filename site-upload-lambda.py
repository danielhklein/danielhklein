import boto3
import zipfile
from io import BytesIO
from botocore.client import Config

def lambda_handler(event, context):
    try:
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
                
        sns = boto3.resource('sns')
        topic_arn = 'arn:aws:sns:us-east-1:654016828638:deployPersonalWebsiteTopic'
        topic = sns.Topic(topic_arn)
        topic.publish(
            Subject='Personal Site Deployed', 
            Message='Site Deployed Successfully'
        )
    except:
        topic.pusblish(
            Subject='Personal Site Deploy Failed',
            Message='Site Deployment Failed'
        )
        raise
    
    return
