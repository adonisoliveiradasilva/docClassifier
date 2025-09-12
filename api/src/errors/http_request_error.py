class HttpRequestError(Exception):
    """
    Classe de erro personalizada para erros de requisição HTTP
    """
    def __init__(self, message:str, status_code:int) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
