from flask_restful import Resource, reqparse, fields, marshal_with
from services import team_service, user_service
from auth import jwt_required, get_jwt_identity
from common.utils import validate_country_name


team_patch_parser = reqparse.RequestParser()
team_patch_parser.add_argument("team_name", help="Team name")
team_patch_parser.add_argument("country", help="Team Country")


class Team(Resource):

    @jwt_required
    def get(self):
        """
        Returns the team
        :return: team
        """
        user_data = user_service.get_user_data_by_username(get_jwt_identity())
        return user_data.team

    @jwt_required
    def patch(self):
        """
        Update an existing team details.
        Only team name and country can be updated
        :param team_id: team id of the team to be updated
        :return: updated team object
        """
        args = team_patch_parser.parse_args()
        validate_country_name(args.country)
        return team_service.update_team_details(team_name=args.team_name,
                                                country=args.country)
