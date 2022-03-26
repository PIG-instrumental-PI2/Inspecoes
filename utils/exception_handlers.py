from fastapi import Request, status
from fastapi.responses import JSONResponse


class BaseCustomException(Exception):
    """Base for custom exceptions"""

    message = ""
    status_code = status.HTTP_400_BAD_REQUEST


class BadRequestException(BaseCustomException):
    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        self.status_code = status_code
        self.message = message


class InternalServerError(BaseCustomException):
    def __init__(self, message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.status_code = status_code
        self.message = message


class ExceptionHandler(Exception):
    """Class to handle known exceptions"""

    @staticmethod
    async def exception_handler(request: Request, ex: BaseCustomException):
        try:
            status_code = ex.status_code
            error_message = ex.message
        except Exception:
            error_message = "An unexpected error occurred"
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        response = {"error": error_message}
        return JSONResponse(status_code=status_code, content=response)
