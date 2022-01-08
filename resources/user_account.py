from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash
from common.utils import is_valid_email

from auth import (
    create_jwt,
    jwt_required,
    get_jwt_identity
)
from common.utils import format_url
from config import app_config
from config.errors import (
    UserNotFoundException,
    InvalidUserCredentialsException
)
from services import user_service

login_request_parser = reqparse.RequestParser()
login_request_parser.add_argument("username", help="Missing username", required=True)
login_request_parser.add_argument("password", help="Missing password", required=True)


def _make_response(jwt_token):
    return {
        "jwt_token": jwt_token,
        "team_url": format_url(app_config.TEAM_URL),
        "players_url": format_url(app_config.PLAYERS_URL),
        "transfers_url": format_url(app_config.TRANSFERS_URL),
        "logout_url": format_url(app_config.LOGOUT_URL)
    }


class UserLogin(Resource):

    def post(self):
        """User login/Authentication"""
        args = login_request_parser.parse_args()
        is_valid_email(args.username)

        if not user_service.check_if_user_exists(args.username):
            raise UserNotFoundException(payload=args)

        user = user_service.get_user_by_username(args.username)
        if not user or not check_password_hash(user.password, args.password):
            raise InvalidUserCredentialsException(payload=args)

        user_login = user_service.get_login(args.username)
        if user_login:
            user_service.remove_login(user_login)

        jwt_token = create_jwt(identity=args.username)
        return _make_response(jwt_token)


class UserLogout(Resource):

    @jwt_required
    def post(self):
        user_session = user_service.get_login(get_jwt_identity())
        user_service.remove_login(user_session)
        return {"login_url": format_url(app_config.LOGIN_URL)}
