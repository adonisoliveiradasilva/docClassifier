from typing import Callable, Union, Dict
from fastapi import Request as RequestFastApi

# pylint: disable=broad-exception-caught
async def request_adapter(request: Union[RequestFastApi, Dict], callback: Callable):
    """
    Adapta uma requisição FastAPI ou um dicionário para o formato esperado pelo controlador,
    chamando o callback correspondente.

    """
    body = None
    if isinstance(request, RequestFastApi):
        try:
            body = await request.json()
        except Exception as e:
            print(f"Erro ao ler JSON: {e}")
            body = {}

        http_request = {
            "query_params": request.query_params,
            "body": body
        }
    else:
        http_request = request
    try:
        http_response = callback(http_request)
        return http_response
    except Exception as e:
        return None
