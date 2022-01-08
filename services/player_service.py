from repositories import player_repository
from domain.data import Player
from common.utils import currency_formatter, format_url
from config import app_config


def get_players_by_team(team_id):
    """
    Returns players on given team
    :param team_id: Team ID
    :return: List[Player]
    """
    players = player_repository.get_players_for_team(team_id)
    return [player_model_to_player_data(player) for player in players]


def player_model_to_player_data(player):
    """player model to player domain objects"""
    player_data = Player(
        player_id=player.id,
        first_name=player.first_name,
        last_name=player.last_name,
        age=player.age,
        country=player.country,
        market_value=currency_formatter(player.market_value),
        team_id=player.team_id,
        player_type=player.player_type,
        player_url=format_url(app_config.PLAYER_URL.format(player.id))
    )
    return player_data


def update_player_details(player_id, first_name=None, last_name=None, country=None):
    """
    Update player details as supplied
    :param player_id: player id
    :param first_name: First Name
    :param last_name: Last Name
    :param country: Country
    :return: updated player object
    """
    player = player_repository.update_player_details(player_id, first_name, last_name, country)
    return player_model_to_player_data(player)
