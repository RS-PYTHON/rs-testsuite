from behave import given, when, then
import os
import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError


@given('s3 access is configured')
def step_check_s3_configuration(context):
    """Checks that all variable are set to check s3 configuration"""
    assert 'S3_ACCESS_KEY' in os.environ, "S3_ACCESS_KEY environment variable is not set."
    assert 'S3_SECRET_ACCESS_KEY' in os.environ, "S3_SECRET_ACCESS_KEY environment variable is not set."
    assert 'S3_DOMAIN_URL' in os.environ, "S3_DOMAIN_URL environment variable is not set."

    context.s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY'),
        endpoint_url=os.getenv('S3_DOMAIN_URL')
    )


@given('the s3 bucket {bucket} exists')
def step_s3_bucket_exist(context, bucket: str):
    assert s3_bucket_existence(context, bucket) is True, f"The bucket {bucket} does not exist."


@given('the s3 bucket {bucket} does not exist')
def step_s3_bucket_dont_exist(context, bucket: str):
    assert s3_bucket_existence(context, bucket) is False, f"The bucket {bucket} exists."


@then('the file {file_path} exists on the s3 bucket {bucket}')
@given('the file {file_path} exists on the s3 bucket {bucket}')
def step_s3_file_bucket_exist(context, file_path: str, bucket: str):
    assert s3_file_bucket_existence(context, file_path, bucket) is True, \
        f"The file {file_path} does not exist on the bucket {bucket}."


@then('the file {file_path} does not exist on the s3 bucket {bucket}')
@given('the file {file_path} does not exist on the s3 bucket {bucket}')
def step_s3_file_bucket_dont_exist(context, file_path: str, bucket: str):
    assert s3_file_bucket_existence(context, file_path, bucket) is False, \
        f"The file {file_path} exist on the bucket {bucket}."


def s3_bucket_existence(context, bucket: str) -> bool:
    """Return true if the S3 bucket exists."""
    """Check that the clientis set on the context"""
    assert context.s3_client is not None, "s3 client is not configured (call 'given s3 access is configured' first)."
    result = False
    try:
        context.s3_client.head_bucket(Bucket=bucket)
        result = True
    except ClientError:
        result = False

    return result


def s3_file_bucket_existence(context, file_path: str, bucket: str) -> bool:
    """Return true if the file_path exists on the S3 bucket."""
    """Check that the clientis set on the context"""
    assert context.s3_client is not None, "s3 client is not configured (call 'given s3 access is configured' first)."
    result = False
    try:
        context.s3_client.head_object(Bucket=bucket, Key=file_path)
        result = True
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            result = False
        else:
            raise e

    return result


@when('the file {file_path} is created on the s3 bucket {bucket}')
def step_s3_file_creation(context, file_path: str, bucket: str):
    assert context.s3_client is not None, "s3 client is not configured (call 'given s3 access is configured' first)."

    # Create local file
    with open("temp.txt", 'w') as file:
        file.write("FAKE content for file " + file_path)

    # Upload on the bucket S3
    try:
        context.s3_client.upload_file("temp.txt", bucket, file_path)
    except FileNotFoundError:
        assert False, f"file {file_path} is unreachable."
    except NoCredentialsError:
        assert False, "Bad S3 credentials."


@when('the file {file_path} is deleted from the s3 bucket {bucket}')
def step_s3_file_deletion(context, file_path: str, bucket: str):
    assert context.s3_client is not None, "s3 client is not configured (call 'given s3 access is configured' first)."

    # Delete the file
    try:
        context.s3_client.delete_object(Bucket=bucket, Key=file_path)
    except ClientError:
        assert False, f"Error while deleting the file {file_path}."
    except NoCredentialsError:
        assert False, "Bad S3 credentials."
