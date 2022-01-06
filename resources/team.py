from flask_restful import Resource, reqparse, fields, marshal_with
from services import team_service, user_service
from auth import jwt_required, get_jwt_identity


team_patch_parser = reqparse.RequestParser()
team_patch_parser.add_argument("team_name", help="Team name")
team_patch_parser.add_argument("country", help="Team Country")

team_fields = {
    "team_id": fields.Integer,
    "team_name": fields.String,
    "available_cash": fields.String,
    "country": fields.String,
    "account_id": fields.Integer,
    "team_value": fields.String
}


class Team(Resource):

    @jwt_required
    @marshal_with(team_fields)
    def get(self):
        """
        Returns the team
        :return: team
        """
        user_data = user_service.get_user_data_by_username(get_jwt_identity())
        return user_data.team

    @jwt_required
    @marshal_with(team_fields)
    def patch(self):
        """
        Update an existing team details.
        Only team name and country can be updated
        :param team_id: team id of the team to be updated
        :return: updated team object
        """
        args = team_patch_parser.parse_args()
        return team_service.update_team_details(team_name=args.team_name,
                                                country=args.country)
