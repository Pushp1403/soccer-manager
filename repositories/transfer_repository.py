from domain.data import Transfer as TransferData, UserData
from model.models import Transfer as TransferModel
from config.app_config import db
from repositories import user_repository, team_repository, player_repository
from common.utils import adjust_market_value


def create_new_transfer(transfer: TransferData):
    """
    Creates a new transfer on transfer list
    :param transfer: Transfer Object
    :return: transfer ID
    """
    new_transfer = TransferModel(
        player_id=transfer.player_id,
        ask_price=transfer.ask_price,
        transferred=transfer.transferred,
        transferred_from=transfer.transferred_from
    )
    db.session.add(new_transfer)
    db.session.commit()
    return new_transfer.id


def get_all_active_transfers():
    """
    Get All active transfers
    :return: List of active transfers
    """
    return TransferModel.query.filter_by(transferred=False).all()


def get_transfer_by_id(transfer_id):
    """Returns a transfer by transfer_id"""
    return TransferModel.query.filter_by(id=transfer_id).first()


def confirm_transfer(transfer_id: int, buyer: UserData):
    """
    Confirms a transfer
    :param transfer_id: transfer ID
    :param buyer: buyer
    :return: None
    """
    db.session.close()
    with db.session.begin():
        # set the transferred flag to True
        transfer = get_transfer_by_id(transfer_id)
        transfer.transferred = True
        transfer.transferred_to = buyer.team.team_id

        # Update team and market_value on the player
        player = player_repository.get_player_by_id(transfer.player_id)
        player.team_id = buyer.team.team_id
        player.market_value = adjust_market_value(transfer.ask_price)

        # deduct team budget by player's ask price
        buyer_team = team_repository.get_team_by_team_id(buyer.team.team_id)
        buyer_team.available_cash -= transfer.ask_price

        # add player's price in seller's team budget
        seller_team = team_repository.get_team_by_team_id(transfer.transferred_from)
        seller_team.available_cash += transfer.ask_price
