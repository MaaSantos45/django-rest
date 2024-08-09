from rest_framework.exceptions import APIException as DRFAPIException
from rest_framework import status


class ApiException(DRFAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'An error occurred.'
    default_code = 'api_exception'

    def __init__(self, detail=None, status_code=None):
        if status_code is not None:
            self.status_code = status_code

        if detail is not None:
            self.default_detail = detail
