import shutil
import shutil
from respond import initialize_chat_engine
import os
import boto3
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv()


def initialize_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION"),
    )
    return s3


s3 = initialize_s3()


def upload_file(file_path):
    bucket_name = "edgardatafiles"
    file_name = os.path.basename(file_path)
    try:
        s3.upload_file(
            file_path,
            bucket_name,
            file_name,
            # ExtraArgs={"ACL": "public-read"},
        )

        print(f"Upload Successful: {file_name}")
    except FileNotFoundError:
        print(f"The file was not found: {file_name}")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None

    # Generate a pre-signed URL for the uploaded file
    file_url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": file_name},
        ExpiresIn=3600,  # URL expires in 1 hour
    )

    initialize_chat_engine()

    return file_url, file_name
