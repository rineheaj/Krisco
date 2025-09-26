from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from pathlib import Path
from datetime import datetime, timedelta
import json
import os

from models import Photo
from extensions import db
from blueprints.gallery import gallery_bp
from blueprints.upload import upload_bp
from blueprints.guestbook import guestbook_bp

from github_file_services import (
    save_guestbook_github,
    read_guestbook_github,
    save_guestbook_github_json,
    read_guestbook_json_github,
    save_uploaded_image_to_github
)

UPLOAD_FOLDER = Path(__file__).parent / "static" / "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

IMAGES_FOLDER = Path(__file__).parent / "static" / "images"
IMAGE_SUFFIXES = {".jpg", ".png", ".jpeg", ".gif"}
GUEST_BOOK = Path(__file__).parent / "data" / "guestbook.txt"


def create_app():
    app = Flask(__name__)
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = timedelta(days=2)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change")

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(gallery_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(guestbook_bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    with app.app_context():
        db.create_all()
        for img in IMAGES_FOLDER.iterdir():
            if img.suffix.lower() in IMAGE_SUFFIXES:
                if not Photo.query.filter_by(filename=img.name).first():
                    db.session.add(Photo(filename=img.name))
                    print(f"🟢 Added {img.name}")
        db.session.commit()

    return app



#OLD DONT DELETE YET
# @app.route("/story")
# def story():
#     return render_template("story.html")


# @app.route("/messages")
# def messages():
#     return render_template("messages.html")


# @app.route("/guestbook_local_json", methods=["GET", "POST"])
# def guestbook_local_json():
#     filepath = "data/guestbook.json"
#     if not os.path.exists(filepath):
#         os.makedirs(os.path.dirname(filepath), exist_ok=True)
#         with open(filepath, mode="w", encoding="utf-8") as outfile:
#             json.dump([], outfile)

#     if request.method == "POST":
#         name = request.form.get("name")
#         message = request.form.get("message")
#         if name and message:
#             new_entry = {
#                 "timestamp": datetime.now().strftime("%m-%d-%Y %H:%M:%S"),
#                 "name": name,
#                 "message": message,
#             }
#             with open(filepath, mode="r", encoding="utf-8") as infile:
#                 entries = json.load(infile)
#             entries.append(new_entry)

#             try:
#                 with open(filepath, mode="w", encoding="utf-8") as outfile:
#                     json.dump(entries, outfile, indent=2)
#                 print(f"✅ Saved json to {filepath}")
#             except Exception as e:
#                 print(f"⚠️ Could not save local guestbook.json {e}")

#             return redirect(url_for("guestbook_local_json"))

#     # GET REQUEST
#     with open("data/guestbook.json", mode="r", encoding="utf-8") as infile:
#         entries = json.load(infile)
#     entries = list(reversed(entries))

#     if not entries:
#         print("❌ No entries in json guestbook")
#     else:
#         for entry in entries:
#             print(f"🟢 {entry}")

#     return render_template("guestbook.html", entries=entries)


# @app.route("/guestbook_json", methods=["GET", "POST"])
# def guestbook_json():
#     if request.method == "POST":
#         name = request.form.get("name")
#         message = request.form.get("message")
#         if name and message:
#             try:
#                 save_guestbook_github_json(name, message)
#             except Exception as e:
#                 print(f"⚠️ Failed to save to GitHub: {e}")
#             return redirect(url_for("guestbook_json"))

#     entries = read_guestbook_json_github()
#     for e in entries:
#         print(f"🟢 {e}")
#     return render_template("guestbook.html", entries=entries)




# @app.route("/.well-known/appspecific/com.chrome.devtools.json")
# def devtools():
#     ua = request.headers.get("User-Agent", "HUH AGENT").lower()
#     print(ua)
#     if "chrome" in ua:
#         return "", 204
#     else:
#         return jsonify(
#             {
#                 "status_code": 200,
#                 "response_text": "Running in a local environment. This endpoint is for Chrome DevTools.",
#             }
#         ), 200


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
    # app.run(debug=True)
