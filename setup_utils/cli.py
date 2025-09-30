import click
import getpass
from flask.cli import with_appcontext
from setup_utils.models import db, Photo, User
from setup_utils.constants import IMAGES_FOLDER, IMAGE_SUFFIXES, UPLOAD_FOLDER

import subprocess


@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()
    for folder in (IMAGES_FOLDER, UPLOAD_FOLDER):
        for img in folder.iterdir():
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


@click.command("purge-photo")
@click.argument("filename")
@with_appcontext
def purge_photo_command(filename):
    if not click.confirm(
        f"⚠️ This will delete <{filename}> from the DB and run <git rm>\nContinue?"
    ):
        click.echo("❌ Aborted.")
        return

    photo = Photo.query.filter_by(filename=filename).first()
    if photo:
        db.session.delete(photo)
        db.session.commit()
        click.echo(f"🗑️ Deleted DB entry for {filename}")
    else:
        click.echo(f"⚠️ No DB entry found for {filename}")

    try:
        subprocess.run(["git", "rm", f"{UPLOAD_FOLDER}/{filename}"], check=True)
        click.echo(f"✅ Ran <git rm {UPLOAD_FOLDER}/{filename}>")
    except subprocess.CalledProcessError as e:
        click.echo(f"❌ Git error: {e}")


# USERSTUFF
@click.command("create-user")
@with_appcontext
def create_user_command():
    username = click.prompt("Enter a username")

    while (password := getpass.getpass("Enter a password: ")) != (
        confirm := getpass.getpass("Confirm password: ")
    ) or not password:
        click.echo("⚠️ Passwords do not match or are empty. Try again")
    print(f"✅ Passwords match adding {username} to the DB.")

    if User.query.filter_by(username=username).first():
        click.echo(f"⚠️ User '{username}' already exists.")
        return

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo(f"✅ Created user '{username}'")


@click.command("drop-table")
@click.argument("table_name")
@with_appcontext
def drop_table_command(table_name):
    engine = db.get_engine()

    if not click.confirm(f"⚠️ Are you sure you want to drop the table '{table_name}'?"):
        click.echo("❌ Aborted.")
        return

    try:
        table = db.metadata.tables.get(table_name)
        if table is not None:
            table.drop(engine)
        else:
            click.echo(f"⚠️ Table '{table_name}' not found in metadata")
    except Exception as e:
        print(f"🔴 ERROR: {e}")
