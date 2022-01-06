from flask_restful import Resource, reqparse
from services import transfer_service, user_service
from auth import jwt_required, get_jwt_identity
from config.errors import InvalidTransferException, InsufficientFundsException


new_transfer_request_parse = reqparse.RequestParser()
new_transfer_request_parse.add_argument("player_id",
                                        type=int,
                                        required=True,
                                        help="Player ID is mandatory")

new_transfer_request_parse.add_argument("ask_price",
                                        type=int,
                                        required=True,
                                        help="Please specify an ask price")


class Transfer(Resource):

    @jwt_required
    def post(self):
        """
        Creates a new transfer request
        :return: newly created transfer request
        """
        args = new_transfer_request_parse.parse_args()
        transfer = transfer_service.create_new_transfer(args.player_id, args.ask_price)
        return transfer

    @jwt_required
    def put(self, transfer_id):
        """
        Confirm transfer
        :param transfer_id: transfer id
        :return: Boolean indicating transfer status
        """
        user = user_service.get_user_data_by_username(get_jwt_identity())
        transfer = transfer_service.get_transfer_by_transfer_id(transfer_id)

        if transfer.transferred_from == user.team.team_id:
            raise InvalidTransferException(payload={"transfer_id": transfer_id})

        if user.team.available_cash < transfer.ask_price:
            raise InsufficientFundsException(payload={})

        return transfer_service.confirm_transfer(transfer_id, user)

