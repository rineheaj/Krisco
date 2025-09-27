import click
from flask.cli import with_appcontext
from models import db, Photo
from constants import IMAGES_FOLDER, IMAGE_SUFFIXES



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
