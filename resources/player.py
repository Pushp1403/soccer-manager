from flask_restful import Resource, reqparse
from services import user_service, player_service
from auth import get_jwt_identity, jwt_required
from config.errors import InvalidPlayerIdException

patch_request_parser = reqparse.RequestParser()
patch_request_parser.add_argument("first_name")
patch_request_parser.add_argument("last_name")
patch_request_parser.add_argument("country")


def _find_player(player_id):
    username = get_jwt_identity()
    user_data = user_service.get_user_data_by_username(username)
    players = user_data.team.players
    for player in players:
        if player.player_id == int(player_id):
            return player
    raise InvalidPlayerIdException(payload={"player_id": player_id})


class Player(Resource):

    @jwt_required
    def get(self, player_id):
        """
        Get player with given player id
        :param player_id: Player ID
        :return:
        """
        return _find_player(player_id)

    @jwt_required
    def patch(self, player_id):
        """
        finds and update the player with player id
        :param player_id:  player id
        :return: updated player object
        """
        _find_player(player_id)
        args = patch_request_parser.parse_args()
        player = player_service.update_player_details(
            player_id,
            first_name=args.first_name,
            last_name=args.last_name,
            country=args.country
        )
        return player
