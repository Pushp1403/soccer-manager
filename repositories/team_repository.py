from config.app_config import db
from model.models import Team as TeamModel
from domain.data import Team as TeamData


def create_team(team: TeamData):
    """
    Create Team
    :param team: Team data
    :return: ID of newly created team
    """
    try:
        team = TeamModel(team_name=team.team_name,
                         country=team.country,
                         available_cash=team.available_cash,
                         team_owner=team.account_id)
        db.session.add(team)
        db.session.commit()
    except:
        db.session.rollback()
        raise

    return team.id


def update_team_details(team_id, team_name=None, country=None):
    """
    Update team details as specified
    :param team_id: Optional Team ID
    :param team_name: Optional Name of the team
    :param country: Optional Country
    :return: updated team object
    """
    try:
        existing_team = get_team_by_team_id(team_id)
        existing_team.team_name = team_name or existing_team.team_name
        existing_team.country = country or existing_team.country
        db.session.commit()
    except:
        db.session.rollback()
        raise

    return existing_team


def get_team_by_user_id(user_id):
    """
    Returns the team belonging to user id
    :param user_id: User ID
    :return: Team object
    """
    return TeamModel.query.filter_by(team_owner=user_id).first()


def get_team_by_team_id(team_id):
    """
    Returns a team by team ID
    :param team_id: Team ID
    :return: Team Object
    """
    return TeamModel.query.filter_by(id=team_id).first()
