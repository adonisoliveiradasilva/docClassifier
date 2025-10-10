from pydantic import BaseModel


class ResponseModel(BaseModel):
    """
    Estrutura de resposta default para qualquer rota
    """

    status_code: int
    message: str
    data: dict


class ResponseSuccessModel(ResponseModel):
    """
    Modelo de resposta para requisição executada com sucesso que não retorne informações adicionais no data.
    """

    model_config = {
        "json_schema_extra": {
            "example": {
                "status_code": 200,
                "message": "Success",
                "data": {},
            }
        }
    }


class ResponseErrorModel(ResponseModel):
    """
    Modelo de resposta para requisição executada com erro interno.
    """

    model_config = {
        "json_schema_extra": {
            "example": {
                "status_code": 500,
                "message": "Internal Server Error",
                "data": {},
            }
        }
    }


class ResponseBadRequest(ResponseModel):
    """
    Modelo de resposta para requisição executada com erro na requisição.
    """

    model_config = {
        "json_schema_extra": {
            "example": {
                "status_code": 400,
                "message": "Bad Request",
                "data": {"error": "mensagem com o erro ocorrido"},
            }
        }
    }
