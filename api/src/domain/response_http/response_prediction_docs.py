from .response_base_model import ResponseModel


class ResponseWithPredictionDocs(ResponseModel):
    """
    Modelo de resposta para requisições executadas com sucesso para o modelo de classificação de documentos.
    """

    status_code: int
    message: str
    data: dict

    class Config:
        """
        Exemplo de resposta para requisições executadas com sucesso para o modelo de classificação de documentos.
        """

        schema_extra = {
            "example": {
                "status_code": 200,
                "message": "Operação realizada com sucesso",
                "data": {
                    "predicted_class": "CNH",
                    "confidence": 0.9999999,
                    "all_confidences": {
                        "CNH": 0.9999999,
                        "RG": 0.0000001,
                        "PASSAPORTE": 0.0000001,
                    },
                },
            }
        }
