import os
import mimetypes
import json

import boto3
from botocore.exceptions import ClientError


# =========================
# Configuration
# =========================

REGION = "ap-south-1"

BUCKET_NAME = "static-host19"

WEBSITE_FOLDER = "website"

INDEX_DOCUMENT = "index.html"
ERROR_DOCUMENT = "error.html"


# =========================
# AWS Clients
# =========================

s3 = boto3.client("s3", region_name=REGION)


# =========================
# Create Bucket
# =========================

def create_bucket():

    try:

        s3.head_bucket(Bucket=BUCKET_NAME)

        print(f"Bucket already exists: {BUCKET_NAME}")

    except ClientError as error:

        error_code = error.response["Error"]["Code"]

        if error_code in ["404", "NoSuchBucket"]:

            print(f"Creating bucket: {BUCKET_NAME}")

            s3.create_bucket(
                Bucket=BUCKET_NAME,
                CreateBucketConfiguration={
                    "LocationConstraint": REGION
                }
            )

            print("Bucket created successfully.")

        else:

            raise


# =========================
# Disable Public Access Block
# =========================

def configure_public_access():

    print("Configuring public access settings...")

    s3.put_public_access_block(

        Bucket=BUCKET_NAME,

        PublicAccessBlockConfiguration={
            "BlockPublicAcls": False,
            "IgnorePublicAcls": False,
            "BlockPublicPolicy": False,
            "RestrictPublicBuckets": False
        }
    )

    print("Public access settings configured.")


# =========================
# Configure Website Hosting
# =========================

def configure_website():

    print("Configuring static website hosting...")

    s3.put_bucket_website(

        Bucket=BUCKET_NAME,

        WebsiteConfiguration={
            "IndexDocument": {
                "Suffix": INDEX_DOCUMENT
            },

            "ErrorDocument": {
                "Key": ERROR_DOCUMENT
            }
        }
    )

    print("Static website hosting enabled.")


# =========================
# Create Bucket Policy
# =========================

def create_bucket_policy():

    print("Creating bucket policy...")

    policy = {

        "Version": "2012-10-17",

        "Statement": [

            {
                "Sid": "PublicReadGetObject",

                "Effect": "Allow",

                "Principal": "*",

                "Action": "s3:GetObject",

                "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*"
            }
        ]
    }

    s3.put_bucket_policy(

        Bucket=BUCKET_NAME,

        Policy=json.dumps(policy)
    )

    print("Bucket policy created.")


# =========================
# Upload Website Files
# =========================

def upload_website():

    print("\nUploading website files...\n")

    for root, directories, files in os.walk(WEBSITE_FOLDER):

        for file_name in files:

            local_path = os.path.join(
                root,
                file_name
            )

            s3_key = os.path.relpath(
                local_path,
                WEBSITE_FOLDER
            )

            content_type, _ = mimetypes.guess_type(
                local_path
            )

            if content_type is None:

                content_type = "application/octet-stream"

            print(
                f"Uploading: {local_path} "
                f"-> {s3_key} "
                f"({content_type})"
            )

            s3.upload_file(

                local_path,

                BUCKET_NAME,

                s3_key,

                ExtraArgs={
                    "ContentType": content_type
                }
            )

    print("\nAll website files uploaded successfully.")


# =========================
# Display Website URL
# =========================

def display_website_url():

    website_url = (
        f"http://{BUCKET_NAME}.s3-website-"
        f"{REGION}.amazonaws.com"
    )

    print("\n====================================")
    print("Deployment completed successfully!")
    print("====================================")

    print(f"\nBucket: {BUCKET_NAME}")

    print(f"\nWebsite URL:")
    print(website_url)


# =========================
# Main
# =========================

def main():

    print("\nStarting S3 website deployment...\n")

    create_bucket()

    configure_public_access()

    configure_website()

    create_bucket_policy()

    upload_website()

    display_website_url()


if __name__ == "__main__":
    main()
