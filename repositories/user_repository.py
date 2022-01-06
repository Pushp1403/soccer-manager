from config.app_config import db
from domain.data import UserData
from model.models import User, Team, Player, UserLogin


def check_user(username):
    """Checks if a user with provided username exists"""
    exists = db.session.query(
        User.query.filter_by(username=username).exists()
    ).scalar()
    db.session.close()
    return exists


def get_user_by_username(username):
    """Returns user by username"""
    return User.query.filter_by(username=username).first()


def register_user(user_data: UserData):
    """
    Creates a new user, Team and players
    :param user_data: User data
    :return: newly created user
    """
    with db.session.begin():
        user = User(
            username=user_data.username,
            password=user_data.password
        )

        team = Team(
            team_name=user_data.team.team_name,
            country=user_data.team.country,
            available_cash=user_data.team.available_cash,
            team_owner=user.id
        )

        user.team = team
        players = list()
        for player in user_data.team.players:
            player_to_add = Player(
                first_name=player.first_name,
                last_name=player.last_name,
                player_type=player.player_type,
                market_value=player.market_value,
                age=player.age,
                country=player.country,
                team_id=team.id
            )
            players.append(player_to_add)
        team.players = players

        db.session.add(user)
        db.session.add(team)
        db.session.add_all(players)

    return user_data


def create_login(username, token):
    """Creates an active session record"""
    login = UserLogin(username=username, token=token)
    db.session.add(login)
    db.session.commit()


def get_login_by_username(username):
    """Returns, if exists an active session for the user"""
    return UserLogin.query.filter_by(username=username).first()


def remove_login(user_login):
    """Delete the session"""
    UserLogin.query.filter_by(id=user_login.id).delete()
    db.session.commit()
