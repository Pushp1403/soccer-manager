from repositories import team_repository
from domain.data import Team
from common.utils import currency_formatter
from services import user_service, player_service
from auth import get_jwt_identity


def get_team_by_team_id(team_id):
    """
    Returns a team by team id
    :param team_id: team id
    :return: team object
    """
    team = team_repository.get_team_by_team_id(team_id)
    return _team_model_to_team_data(team)


def get_team_by_user(user_id):
    """
    Returns a team for the user
    :param user_id: user id
    :return: team
    """
    team = team_repository.get_team_by_user_id(user_id)
    team_data = _team_model_to_team_data(team)
    return team_data


def update_team_details(team_name=None, country=None):
    """
    update the team details
    :param team_name: team name (optional)
    :param country: (optional)
    :return: updated team object
    """
    user_data = user_service.get_user_data_by_username(get_jwt_identity())
    team = team_repository.update_team_details(user_data.team.team_id, team_name=team_name, country=country)
    return _team_model_to_team_data(team)


def _team_model_to_team_data(team):
    team_data = Team(
        team_id=team.id,
        team_name=team.team_name,
        available_cash=currency_formatter(team.available_cash),
        country=team.country,
        account_id=team.team_owner,
        team_value=currency_formatter(sum(player.market_value for player in team.players))
    )

    team_data.players = [player_service.player_model_to_player_data(player) for player in team.players]
    return team_data
