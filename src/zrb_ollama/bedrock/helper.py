import boto3

from ..config import AWS_ACCESS_KEY, AWS_DEFAULT_REGION, AWS_SECRET_ACCESS_KEY


def create_bedrock_client(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_region_name=AWS_DEFAULT_REGION,
):
    return boto3.client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        service_name="bedrock-runtime",
        region_name=aws_region_name,
    )
