from dataclasses import dataclass

from api.src.domain.enums.document_type import DocumentTypeEnum


@dataclass
class PredictionResult:
    """
    Representa o resultado da predição de um documento.
    """

    user_expected_type: DocumentTypeEnum
    model_predicted_type: DocumentTypeEnum
    confidence_score: float
    is_match: bool
