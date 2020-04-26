import boto3

S3 = boto3.client('s3')


def list_s3_buckets():
    """Fetch S3 bucket of the current AWS connexion"""
    buckets = S3.list_buckets()
    return buckets['Buckets']
