from abc import ABC
from typing import Union
from fastapi.responses import JSONResponse


class ResponseHTTP(ABC):
    """
    Interface para as respostas HTTP.

    Args:
        status_code: o código de status da resposta HTTP.
        message: mensagem que descreve o significado do código HTTP.
    """

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message

    def validate(self, status_code: int) -> bool:
        """
        Método responsável por validar se o código gerado pela aplicação corresponde ao Response implementado.

        Args:
            status_code: o código de status da resposta HTTP gerado no processo.

        Returns:
            Booleano indicando se houve a correspondência.
        """
        if status_code == self.status_code:
            return True
        return False

    def response(self, data: Union[dict, None] = None, message: str = None) -> JSONResponse:
        """
        Método responsável por criar o body da resposta à solicitação realizada a aplicação.

        Args:
            data: Qualquer informação adicional que deva ser enviada na resposta HTTP. Default None.

        Returns:
            Objeto JSONResponse com as chaves status_code, message e data.
        """
        data = {} if data is None else data
        return JSONResponse(
            status_code=self.status_code,
            content={
                "status_code": self.status_code,
                "message": message or self.message,
                "data": data,
            },
        )
