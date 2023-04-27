from flask import Flask, render_template
from flask_bootstrap import Bootstrap5

import os

basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )
    app.config.from_prefixed_env()

    # app.config.from_pyfile(config_filename)

    # from yourapplication.model import db
    # db.init_app(app)

    # from yourapplication.views.admin import admin
    # from yourapplication.views.frontend import frontend
    # app.register_blueprint(admin)
    # app.register_blueprint(frontend)

    # # WEBSITE_HOSTNAME exists only in production environment
    # if 'WEBSITE_HOSTNAME' not in os.environ:
    #     # local development, where we'll use environment variables
    #     print("Loading config.development and environment variables from .env file.")
    #     app.config.from_object('azureproject.development')
    # else:
    #     # production
    #     print("Loading config.production.")
    #     app.config.from_object('azureproject.production')
    bootstrap = Bootstrap5(app)
    from .auth import bp as auth_bp
    from .controllers.main import bp as main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    from .models import db

    # configure the SQLite database, relative to the app instance folder
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"sqlite:///{os.path.join(basedir, 'data.sqlite')}"
    # initialize the app with the extension

    # Initialize the database
    db.init_app(app)
    from .models.user import User

    with app.app_context():
        db.create_all()

    return app


app = create_app()

"""
404 Page not found error default handler
"""


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html", error=e), 404


# @app.get("/")
# def index():
#     return render_template("index.html")
