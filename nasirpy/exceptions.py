class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str = None):
        self.status_code = status_code
        self.detail = detail or self._get_default_detail(status_code)

    def _get_default_detail(self, status_code: int) -> str:
        return {
            404: "Not Found",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            500: "Internal Server Error"
        }.get(status_code, "Unknown Error")

class NotFoundError(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(404, detail)

class BadRequestError(HTTPException):
    def __init__(self, detail: str = None):
        super().__init__(400, detail)
