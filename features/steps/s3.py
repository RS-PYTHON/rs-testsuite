from behave import given
import os
import boto3
from botocore.exceptions import ClientError


@given('s3 access is configured')
def step_check_s3_configuration(context):
    """Checks that all variable are set to check s3 configuration"""
    assert 'S3_ACCESS_KEY' in os.environ, "S3_ACCESS_KEY environment variable is not set."
    assert 'S3_SECRET_ACCESS_KEY' in os.environ, "S3_SECRET_ACCESS_KEY environment variable is not set."
    assert 'S3_DOMAIN_URL' in os.environ, "S3_DOMAIN_URL environment variable is not set."

    context.s3_access_key = os.getenv('S3_ACCESS_KEY')
    context.s3_secret_access_key = os.getenv('S3_SECRET_ACCESS_KEY')
    context.s3_domain_url = os.getenv('S3_DOMAIN_URL')


@given('the s3 bucket {bucket} exists')
def step_s3_bucket_exist(context, bucket: str):
    assert (step_s3_bucket_existence(context, bucket) is True)


@given('the s3 bucket {bucket} does not exist')
def step_s3_bucket_dont_exist(context, bucket: str):
    assert (step_s3_bucket_existence(context, bucket) is False)


def step_s3_bucket_existence(context, bucket: str) -> bool:
    """
        Return true if the S3 bucket exists.
    """
    """Checks that all variable are set to the context"""
    assert context.s3_access_key is not None, "s3_access_key is not set on the execution context."
    assert context.s3_secret_access_key is not None, "s3_secret_access_key is not set on the execution context."
    assert context.s3_domain_url is not None, "s3_domain_url is not set on the execution context."

    """Connect to the bucket"""
    s3_client = boto3.client(
        's3',
        aws_access_key_id=context.s3_access_key,
        aws_secret_access_key=context.s3_secret_access_key,
        endpoint_url='https://oss.eu-west-0.prod-cloud-ocb.orange-business.com'
    )
    result = False
    try:
        s3_client.head_bucket(Bucket=bucket)
        result = True
    except ClientError:
        result = False

    return result
