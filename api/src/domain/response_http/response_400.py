from .interfaces import ResponseHTTP


class ResponseHTTP400(ResponseHTTP):
    """
    Classe responsável por construir a resposta para solicitações em que o servidor não pode ou não irá processar a
    requisição devido a algo que foi entendida como um erro do cliente.
    """

    def __init__(self, status_code: int = 400, message: str = "Bad request") -> None:
        super().__init__(status_code=status_code, message=message)
