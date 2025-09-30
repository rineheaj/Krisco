from flask import Flask

import os

from setup_utils.models import db, cache, login_manager
from setup_utils.config import Config
from setup_utils.cli import (
    init_db_command,
    count_photos_command,
    clean_orphans_command,
    delete_photo_command,
    rename_photo_command,
    purge_photo_command,
    create_user_command,
    drop_table_command,
)
from setup_utils.constants import UPLOAD_FOLDER
from blueprints import all_blueprints


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    cache.init_app(app)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Register blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    app.cli.add_command(init_db_command)
    app.cli.add_command(count_photos_command)
    app.cli.add_command(rename_photo_command)
    app.cli.add_command(delete_photo_command)
    app.cli.add_command(clean_orphans_command)
    app.cli.add_command(purge_photo_command)
    app.cli.add_command(create_user_command)
    app.cli.add_command(drop_table_command)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
    # app.run(debug=True)
