from typing import Union, List, Type
from fastapi.responses import JSONResponse
from api.src.domain.response_http.interfaces import ResponseHTTP


class ResponseHTTPHandler:
    """
    Classe responsável por criar o body para as solicitações à aplicação.
    """

    @staticmethod
    def create(status_code: int, data: Union[dict, None] = None, message: str = None) -> Union[JSONResponse, None]:
        """
        Cria o conteúdo das respostas.

        Args:
            status_code: código de status gerado pelo processo
            data: informações complementares a serem enviadas. Default None.

        Returns:
            JSONResponse com as chaves status_code, message e data.
        """
        responses: List[Type[ResponseHTTP]] = ResponseHTTP.__subclasses__()
        for response in responses:
            model = response()  # type: ignore[call-arg] # noqa: F821
            if model.validate(status_code=status_code):
                return model.response(data=data, message=message)
        return None
