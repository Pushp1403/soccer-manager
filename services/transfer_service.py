from repositories import transfer_repository, player_repository
from services import user_service
from domain.data import Transfer
from model.models import Transfer as TransferModel
from common.utils import currency_formatter, format_url
from config import app_config
from config.errors import InvalidTransferException
from auth import get_jwt_identity


def confirm_transfer(transfer_id, user_data):
    """
    Execute a transfer transaction
    :param transfer_id: transfer ID
    :param user_data: user data
    :return: completed transfer object
    """
    transfer = _validate_transfer_request(transfer_id)
    transfer_repository.confirm_transfer(transfer_id, user_data)
    return _transfer_model_to_data(transfer)


def get_transfer_by_transfer_id(transfer_id):
    """
    Returns transfer details by transfer ID
    :param transfer_id: transfer ID
    :return:
    """
    transfer = _validate_transfer_request(transfer_id)
    return _transfer_model_to_data(transfer)


def _validate_transfer_request(transfer_id):
    transfer = transfer_repository.get_transfer_by_id(transfer_id)
    if not transfer:
        raise InvalidTransferException(message="Invalid transfer request",
                                       payload={"transfer_id": transfer_id},
                                       status_code=404)
    return transfer


def get_all_active_transfers():
    """
    Get all active transfers
    :return: List of transfers
    """
    all_transfers = transfer_repository.get_all_active_transfers()
    transfer_data = [_transfer_model_to_data(transfer) for transfer in all_transfers]
    return transfer_data


def _transfer_model_to_data(transfer: TransferModel):
    player = player_repository.get_player_by_id(transfer.player_id)
    return Transfer(
        transfer_id=transfer.id,
        player_id=transfer.player_id,
        transferred_to=transfer.transferred_to,
        transferred_from=transfer.transferred_from,
        transferred=transfer.transferred,
        ask_price=currency_formatter(transfer.ask_price),
        player_name=f'{player.first_name} {player.last_name}',
        transfer_url=format_url(app_config.TRANSFER_URL.format(transfer.id))
    )


def create_new_transfer(player_id, ask_price):
    """
    Create new transfer on transfer list
    :param player_id: Player ID
    :param ask_price: ask_price
    :return: newly created transfer
    """
    username = get_jwt_identity()
    user = user_service.get_user_data_by_username(username)
    player = player_repository.get_player_by_id(player_id)

    transfer = Transfer(
        transferred_from=user.team.team_id,
        ask_price=ask_price,
        player_id=player_id,
        transferred=False,
        player_name=f'{player.first_name} {player.last_name}'
    )

    transfer_id = transfer_repository.create_new_transfer(transfer)
    transfer.transfer_id = transfer_id
    transfer.ask_price = currency_formatter(transfer.ask_price)
    transfer.transfer_url = format_url(app_config.TRANSFER_URL.format(transfer_id))
    return transfer
