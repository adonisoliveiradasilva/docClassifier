from .interfaces import ResponseHTTP


class ResponseHTTP200(ResponseHTTP):
    """
    Classe responsável por construir a resposta para solicitações que ocorreram com sucesso.
    """

    def __init__(self, status_code: int = 200, message: str = "Success") -> None:
        super().__init__(status_code=status_code, message=message)
