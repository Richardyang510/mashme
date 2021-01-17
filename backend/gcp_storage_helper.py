from google.cloud import storage
import os
from os.path import join, dirname
from dotenv import load_dotenv
import mysql_helper

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

BUCKET_NAME = os.environ.get("GCP_BUCKET_NAME")

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def post_upload(youtube_id, stem_tempo, stem_type, bucket_name, source_file_name, destination_file_name):
    """Updates the DB on successful upload and removes the local file"""
    # call insert command to insert a new stem
    mysql_helper.insert_stem(youtube_id, bucket_name, stem_tempo, stem_type, destination_file_name)
    os.remove(source_file_name)


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    # bucket_name = "your-bucket-name"
    # source_blob_name = "storage-object-name"
    # destination_file_name = "local/path/to/file"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)

    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )

# sample usage
# upload_blob(BUCKET_NAME, "test.txt", "text.txt")
# download_blob(BUCKET_NAME, "text.txt", "downloadedtext.txt")
