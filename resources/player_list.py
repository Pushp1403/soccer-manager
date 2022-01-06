from flask_restful import Resource
from services import user_service, player_service
from auth import get_jwt_identity, jwt_required


class Players(Resource):

    @jwt_required
    def get(self):
        """returns a list of players"""
        user_data = user_service.get_user_data_by_username(get_jwt_identity())
        return player_service.get_players_by_team(user_data.team.team_id)
