from flask import Blueprint, render_template, redirect, url_for, current_app
from setup_utils.models import Photo, db, cache
from setup_utils.constants import UPLOAD_FOLDER, GROWTH_THRESHOLDS, STAGE_LABELS
from pathlib import Path



gallery_bp = Blueprint("gallery", __name__, url_prefix="/gallery")


def growth_stage(votes: int) -> int:
    stages = sorted(GROWTH_THRESHOLDS.items(), key=lambda x: x[1])
    current_stage = 0
    for stage, threshold in stages:
        if votes >= threshold:
            current_stage = stage
    return current_stage
    # match votes:
    #     case v if v < 3:
    #         return 0
    #     case v if v < 6:
    #         return 1
    #     case _:
    #         return 2


@gallery_bp.app_template_filter("growth_label")
def growth_stage_filter(votes: int) -> int:
    stage = growth_stage(votes)
    return STAGE_LABELS.get(stage, "❓ Unknown")


# @cache.cached(timeout=15, key_prefix="photo_query")
def get_photos():
    return Photo.query.order_by(Photo.votes.desc()).all()


@gallery_bp.route("/")
def gallery():
    db_photos = []
    print(
        f"App method path: {current_app.root_path}\nUPLOAD FOLDER PATH: {UPLOAD_FOLDER}"
    )
    print("=== GALLERY ROUTE START ===")
    for p in get_photos():
        uploads_path = Path(current_app.root_path) / "static" / "uploads" / p.filename
        images_path = Path(current_app.root_path) / "static" / "images" / p.filename
        
        # Print debug info for each photo
        print(f"DB filename: {p.filename}")
        print(f"Exists in uploads? {uploads_path.exists()}")
        print(f"Exists in images? {images_path.exists()}")
        
        if uploads_path.exists():
            folder = "uploads"
        else:
            folder = "images"
            print(f"Falling back to static/images for {p.filename}")
        
        db_photos.append({
            "filename": p.filename,
            "folder": folder,
            "votes": p.votes
        })
    
    print("Gallery photo list (for template):")
    for img in db_photos:
        print(img)
    print("=== GALLERY ROUTE END ===")
    
    imgs = db_photos
    return render_template("gallery.html", imgs=imgs)



@gallery_bp.route("/vote/<filename>", methods=["POST"])
def vote(filename):
    photo = Photo.query.filter_by(filename=filename).first()
    if photo:
        photo.votes += 1
        db.session.commit()
    return redirect(url_for("gallery.gallery"))
