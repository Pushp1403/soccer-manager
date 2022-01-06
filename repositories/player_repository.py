from typing import List

from config.app_config import db
from model.models import Player as PlayerModel
from domain.data import Player as PlayerData


def add_players(players: List[PlayerData], team_id: int):
    """
    Add the player in DB
    :param players: list of players to add
    :param team_id: team ID
    :return: None
    """
    players_to_add = list()
    for player in players:
        player_to_add = PlayerModel(first_name=player.first_name,
                                    last_name=player.last_name,
                                    player_type=player.player_type,
                                    market_value=player.market_value,
                                    age=player.age,
                                    country=player.country,
                                    team_id=team_id)
        players_to_add.append(player_to_add)
    try:
        db.session.add_all(players_to_add)
        db.session.commit()
    except:
        db.session.rollback()
        raise


def get_player_by_id(player_id):
    """
    Get player by player ID
    :param player_id: player ID
    :return: Player
    """
    return PlayerModel.query.filter_by(id=player_id).first()


def get_players_for_team(team_id):
    """
    Returns all the player in specified team
    :param team_id: Team id
    :return: List of Players
    """
    return PlayerModel.query.filter_by(team_id=team_id).all()


def update_player_details(player_id, first_name, last_name, country):
    """
    Update the player details
    :param player_id: Optional
    :param first_name: Optional
    :param last_name: Optional
    :param country: Optional
    :return: updated Player Object
    """
    player = get_player_by_id(player_id)
    player.first_name = first_name or player.first_name
    player.last_name = last_name or player.last_name
    player.country = country or player.country
    db.session.commit()
    return player
