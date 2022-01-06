from domain.data import Team, Player, UserData, UserLogin
from common.player_types import PlayerType
from common.utils import player_age_generator, currency_formatter, format_url
from config import app_config
from repositories import user_repository


def check_if_user_exists(username):
    """Check if there exists a user with given username"""
    return user_repository.check_user(username)


def get_user_by_username(username):
    """find user by username"""
    user = user_repository.get_user_by_username(username)
    user_data = UserData(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        password=user.password
    )
    return user_data


def get_user_data_by_username(username):
    """find user by username"""
    user = user_repository.get_user_by_username(username)
    user_data = UserData(
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )

    team = user.team
    players = [_player_model_to_player_data(player) for player in team.players]
    team_data = Team(
        team_id=team.id,
        team_name=team.team_name,
        available_cash=currency_formatter(team.available_cash),
        country=team.country,
        account_id=team.team_owner,
        team_value=currency_formatter(sum(player.market_value for player in team.players))
    )

    team_data.players = players
    user_data.team = team_data

    return user_data


def _player_model_to_player_data(player):
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


def create_user(username, password, first_name=None, last_name=None):
    """Creates/registers a new user"""

    team = _create_team(f'team_{first_name}_{last_name}')
    team.players = _create_players()

    user_data = UserData(username=username,
                         first_name=first_name,
                         last_name=last_name,
                         password=password,
                         team=team)

    user = user_repository.register_user(user_data)
    return user


def _create_team(team_name):
    team = Team(team_name=team_name,
                available_cash=5000000
                )
    return team


def _create_players():
    players = list()
    player_map = {
        PlayerType.GOALKEEPER: 3,
        PlayerType.DEFENDER: 6,
        PlayerType.ATTACKER: 5,
        PlayerType.MIDFIELDER: 6
    }

    for player_type, no_of_players in player_map.items():
        players.extend(_create_players_by_position(player_type, no_of_players))

    return players


def _create_players_by_position(player_type, no_of_players):
    return [Player(first_name=player_type.value,
                   last_name=str(i + 1),
                   age=player_age_generator(),
                   market_value=1000000,
                   player_type=player_type.value) for i in
            range(no_of_players)]


def create_login(username, token):
    """
    Create a login record for the authenticated user
    :param username: username
    :param token: JWT token
    :return: None
    """
    user_repository.create_login(username, token)


def get_login(username):
    """
    Query for existing active session
    :param username: username
    :return: UserLogin model
    """
    user_login_data = None
    user_login_model = user_repository.get_login_by_username(username)
    if user_login_model:
        user_login_data = UserLogin(username=user_login_model.username,
                                    token=user_login_model.token,
                                    id=user_login_model.id)
    return user_login_data


def remove_login(user_login):
    """Remove user session"""
    user_repository.remove_login(user_login)
