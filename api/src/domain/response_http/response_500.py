from .interfaces import ResponseHTTP


class ResponseHTTP500(ResponseHTTP):
    """
    Classe responsável por construir a resposta para solicitações em que o servidor encontrou uma condição inesperada e
    foi impedido de atender à solicitação.
    """

    def __init__(self, status_code: int = 500, message: str = "Internal Server Error") -> None:
        super().__init__(status_code=status_code, message=message)
