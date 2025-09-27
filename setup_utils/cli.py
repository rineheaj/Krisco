import click
from flask.cli import with_appcontext
from setup_utils.models import db, Photo
from setup_utils.constants import IMAGES_FOLDER, IMAGE_SUFFIXES



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