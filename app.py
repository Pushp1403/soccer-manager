import os
import click
from common.utils import (
    format_response,
    format_error,
    format_generic_error
)
from flask import Flask, json, make_response
from flask.cli import with_appcontext
from werkzeug.exceptions import HTTPException
from config.app_config import db
from flask_restful import Api
from auth import JWTManager
from resources import (
    user,
    user_account,
    team,
    player,
    transfer,
    transfer_list,
    player_list
)
from config.errors import (
    ApplicationException
)

app = Flask(__name__, instance_relative_config=True)
api = Api(app)


@api.representation('application/json')
def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    resp = make_response(json.dumps(format_response(data, code)), code)
    resp.headers.extend(headers or {})
    return resp


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.errorhandler(ApplicationException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    return format_error(e)


@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    return format_generic_error(e)


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""

    # some deploy systems set the database url in the environ
    db_url = os.environ.get("DATABASE_URL")

    if db_url is None:
        # default to a sqlite database in the instance folder
        db_path = os.path.join(app.instance_path, "soccer_mania.db")
        db_url = f"sqlite:///{db_path}"
        # ensure the instance folder exists
        os.makedirs(app.instance_path, exist_ok=True)

    app.config.from_mapping(
        # default secret that should be overridden in environ or config
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        SQLALCHEMY_DATABASE_URI=db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        JWT_SECRET_KEY="soccer_mania",
        BUNDLE_ERRORS=True
    )

    # initialize jwt manager
    JWTManager(app)

    # Register resources
    register_resources(api)

    # initialize Flask-SQLAlchemy and the init-db command
    db.init_app(app)

    # add CLI command for db-setup
    app.cli.add_command(init_db_command)

    return app


def register_resources(api):
    """Register all the resources"""
    # user account endpoints
    api.add_resource(user.User, "/user")
    api.add_resource(user_account.UserLogin, "/login")
    api.add_resource(user_account.UserLogout, "/logout")
    # Team endpoints
    api.add_resource(team.Team, "/team")
    # Player endpoints
    api.add_resource(player.Player, "/player/<player_id>")
    # Players endpoint
    api.add_resource(player_list.Players, "/players")
    # Transfer endpoints
    api.add_resource(transfer.Transfer, "/transfer", "/transfer/<transfer_id>")
    # Transfers
    api.add_resource(transfer_list.TransferList, "/transfers")


def init_db():
    db.drop_all()
    db.create_all()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        init_db()
    app.run()

