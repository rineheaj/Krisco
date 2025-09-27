import os
from pathlib import Path
from datetime import timedelta


class Config:
    UPLOAD_FOLDER = Path(__file__).parent / "static" / "uploads"

    SEND_FILE_MAX_AGE_DEFAULT = timedelta(days=2)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    UPLOAD_FOLDER = str(UPLOAD_FOLDER)
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change")