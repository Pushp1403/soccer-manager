from flask_restful import Resource
from services import transfer_service
from auth import jwt_required


class TransferList(Resource):

    @jwt_required
    def get(self):
        """
        Get all open transfer requests
        :return: list of open transfers
        """
        return transfer_service.get_all_active_transfers()
