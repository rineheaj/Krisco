from flask import Flask, render_template
import os

from setup_utils.models import db
from setup_utils.config import Config
from setup_utils.cli import init_db_command
from setup_utils.constants import UPLOAD_FOLDER
from blueprints import all_blueprints




def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Register blueprints
    for bp in all_blueprints:
        app.register_blueprint(bp)

    @app.route("/")
    def index():
        return render_template("index.html")

    app.cli.add_command(init_db_command)

    return app





if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
    # app.run(debug=True)
