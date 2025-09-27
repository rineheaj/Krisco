import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from setup_utils.models import Photo, db
from setup_utils.github_file_services import save_uploaded_image_to_github


upload_bp = Blueprint(
    "upload",
    __name__,
    url_prefix="/upload"
)

@upload_bp.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            return "❌ No file selected"
        
        filename = secure_filename(file.filename)

        
        existing = Photo.query.filter_by(filename=filename).first()
        if existing:
            flash("That photo is already in the gallery.")
            return redirect(url_for("gallery.gallery"))

        
        filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.stream.seek(0)
        file.save(filepath)

        file.stream.seek(0)
        save_uploaded_image_to_github(file, filename)

        
        if not Photo.query.filter_by(filename=filename).first():
            db.session.add(Photo(filename=filename))
            db.session.commit()
        
        return redirect(url_for("gallery.gallery"))
    
    return render_template("upload.html")
