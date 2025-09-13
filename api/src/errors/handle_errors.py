from typing import Type, Dict, Any
from api.src.errors import HttpRequestError

def handle_errors(error: Type[Exception]) -> Dict[str, Any]:
    """ 
    Gera um dicinário padronizada para tratamento de erros.
    """
    if isinstance(error, HttpRequestError):
        return {
            "data": { "error": error.message },
            "status_code": error.status_code
        }

    return {
        "data": {"error": str(error)},
        "statusCode": 500
    }
