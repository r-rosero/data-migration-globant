
import os
from dotenv import load_dotenv

ENVIRONMENT = "local" #os.getenv("ENVIRONMENT", "produccion")

if ENVIRONMENT == "local":
    load_dotenv()

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_REGION = os.getenv("S3_REGION")
S3_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
S3_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")