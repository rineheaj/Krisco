from flask import Blueprint, render_template, redirect, url_for
from setup_utils.models import Photo, db
from setup_utils.constants import UPLOAD_FOLDER, IMAGE_SUFFIXES

gallery_bp = Blueprint("gallery", __name__, url_prefix="/gallery")


def growth_stage(votes: int) -> int:
    if votes:
        match votes:
            case v if v < 3:
                return 0
            case v if v < 6:
                return 1
            case _:
                return 2


@gallery_bp.app_template_filter("growth_stage")
def growth_stage_filter(votes: int) -> int:
    return growth_stage(votes)


@gallery_bp.route("/")
def gallery():
    db_photos = []
    for p in Photo.query.order_by(Photo.votes.desc()).all():
        if (UPLOAD_FOLDER / p.filename).exists():
            folder = "uploads"
        else:
            folder = "images"
        db_photos.append({"filename": p.filename, "folder": folder, "votes": p.votes})

    imgs = db_photos
    return render_template("gallery.html", imgs=imgs)


@gallery_bp.route("/vote/<filename>", methods=["POST"])
def vote(filename):
    photo = Photo.query.filter_by(filename=filename).first()
    if photo:
        photo.votes += 1
        db.session.commit()
    return redirect(url_for("gallery.gallery"))
