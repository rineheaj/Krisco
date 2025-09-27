import os
from datetime import timedelta
from .constants import UPLOAD_FOLDER

class Config:
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(days=2)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    UPLOAD_FOLDER = str(UPLOAD_FOLDER)
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change")