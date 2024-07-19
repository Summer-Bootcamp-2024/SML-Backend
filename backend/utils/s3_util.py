import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError
from fastapi import UploadFile, File, HTTPException

load_dotenv()

bucket_name = os.getenv("S3_BUCKET_NAME")
s3_region = os.getenv("S3_REGION")
s3_access_key_id = os.getenv("S3_ACCESS_KEY_ID")
s3_secret_access_key = os.getenv("S3_SECRET_ACCESS_KEY")
default_profile_url = f"https://{bucket_name}.s3.{s3_region}.amazonaws.com/default_profile.png"

class Connect:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=s3_access_key_id,
            aws_secret_access_key=s3_secret_access_key,
        )

    def __enter__(self):
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

async def upload_image_to_s3(image_file: bytes, key_name: str):
    try:
        with Connect() as s3_client:
            s3_client.put_object(
                Body=image_file,
                Bucket=bucket_name,
                Key=key_name,
                ContentType='image/jpeg'
            )
            url = f"https://{bucket_name}.s3.{s3_region}.amazonaws.com/{key_name}"
            return url
    except (NoCredentialsError, PartialCredentialsError, ClientError) as e:
        print(f"Error during image upload: {e}")
        return None

async def create_s3_url(file: UploadFile = File(...)):
    contents = await file.read()
    key_name = file.filename
    url = await upload_image_to_s3(contents, key_name)
    if url:
        return url
    else:
        raise HTTPException(status_code=500, detail="Failed to upload")
