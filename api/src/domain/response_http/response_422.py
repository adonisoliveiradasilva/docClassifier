from .interfaces import ResponseHTTP


class ResponseHTTP422(ResponseHTTP):
    """
    Classe responsável por construir a resposta para indicar que o servidor entende o tipo de conteúdo da entidade da
    requisição, e a sintaxe da requisição esta correta, mas não foi possível processar as instruções presentes.
    """

    def __init__(self, status_code: int = 422, message: str = "Unprocessable Entity") -> None:
        super().__init__(status_code=status_code, message=message)
