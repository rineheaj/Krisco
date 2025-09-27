from flask import Blueprint, render_template, redirect, url_for
from models import Photo, db


gallery_bp = Blueprint(
    "gallery",
    __name__,
    url_prefix="/gallery"
)

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
    photos = Photo.query.order_by(Photo.votes.desc())
    return render_template("gallery.html", imgs=photos)


@gallery_bp.route("/vote/<filename>", methods=["POST"])
def vote(filename):
    photo = Photo.query.filter_by(filename=filename).first()
    if photo:
        photo.votes += 1
        db.session.commit()
    return redirect(url_for("gallery.gallery"))