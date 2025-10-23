from pydantic import BaseModel

from api.src.domain.enums import DocumentTypeEnum

from .base import ResponseModel


class ClassificationResponseModel(BaseModel):
    """
    Modelo de resposta para requisição de classificação de documentos bem-sucedida.
    """

    user_expected_type: DocumentTypeEnum
    model_predicted_type: DocumentTypeEnum
    confidence_score: float
    is_match: bool


class PredictionResponse(ResponseModel):
    """
    Modelo de resposta para requisição de classificação de documentos bem-sucedida.
    """

    data: ClassificationResponseModel
