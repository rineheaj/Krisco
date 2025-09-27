import click
from flask.cli import with_appcontext
from setup_utils.models import db, Photo
from setup_utils.constants import IMAGES_FOLDER, IMAGE_SUFFIXES, UPLOAD_FOLDER



@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()
    for img in IMAGES_FOLDER.iterdir():
        if img.suffix.lower() in IMAGE_SUFFIXES:
            if not Photo.query.filter_by(filename=img.name).first():
                db.session.add(Photo(filename=img.name))
                click.echo(f"🟢 Added {img.name}")
    db.session.commit()
    click.echo("✅ Database is up and images were loaded.")


@click.command("count-photos")
@with_appcontext
def count_photos_command():
    count = Photo.query.count()
    click.echo(f"📷 There are {count} photos in the Render database.")



@click.command("rename-photo")
@click.argument("old_filename")
@click.argument("new_filename")
@with_appcontext
def rename_photo_command(old_filename, new_filename):
    """Rename a photo's filename in the database."""
    photo = Photo.query.filter_by(filename=old_filename).first()
    if photo:
        photo.filename = new_filename
        db.session.commit()
        click.echo(f"✅ Renamed {old_filename} → {new_filename} in DB")
    else:
        click.echo(f"⚠️ No DB entry found for {old_filename}")


@click.command("delete-photo")
@click.argument("filename")
@with_appcontext
def delete_photo_command(filename):
    photo = Photo.query.filter_by(filename=filename).first()
    if photo:
        db.session.delete(photo)
        db.session.commit()
        click.echo(f"🗑️ Deleted DB entry for {filename}")
    else:
        click.echo(f"⚠️ No DB entry found for {filename}")


@click.command("clean-orphans")
@with_appcontext
def clean_orphans_command():
    photos = Photo.query.all()
    removed = 0
    for p in photos:
        in_images = (IMAGES_FOLDER / p.filename).exists()
        in_uploads = (UPLOAD_FOLDER / p.filename).exists()
        if not (in_images or in_uploads):
            db.session.delete(p)
            removed += 1
        db.session.commit()
        click.echo(f"🧹 Removed {removed} orphaned DB entries")

