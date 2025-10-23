from api.src.domain.entities import PredictionResult
from api.src.domain.enums import DocumentTypeEnum
from api.src.infra.logs import logger
from api.src.use_cases.classify_documents.contracts import ModelClassifyDocumentsInterface
from api.src.use_cases.classify_documents.exceptions import InvalidDocumentTypeError, PredictionError


class ClassifyDocuments:
    """
    Classe responsável por orquestrar as funções de classificação dos documentos.
    """

    def __init__(self, model_classifier: ModelClassifyDocumentsInterface) -> None:
        self.__model = model_classifier

    def execute(self, image_bytes: bytes, document_type: DocumentTypeEnum) -> PredictionResult:
        """
        Método responsável por executar a regra de negócio.
        """
        logger.info("[ClassifyDocuments] - iniciando a classificação")

        self.__validate_type_input(document_type)

        try:
            predicted_label, confidence = self.__model.predict(image_bytes)
        except Exception as err:
            raise PredictionError(f"[ClassifyDocuments] - falha ao obter predição do modelo - {err}") from err

        try:
            predicted_type_enum = DocumentTypeEnum(str(predicted_label).lower())
        except ValueError as err:
            raise PredictionError(f"[ClassifyDocuments] - classe predita desconhecida: {predicted_label}") from err

        is_correct = predicted_type_enum == document_type

        return PredictionResult(
            user_expected_type=document_type,
            model_predicted_type=predicted_type_enum,
            confidence_score=confidence,
            is_match=is_correct,
        )

    def __validate_type_input(self, document_type: DocumentTypeEnum) -> None:
        """
        Valida se o tipo de documento informado pelo usuário é permitido pelo modelo.
        """
        classes = [doc_type.lower() for doc_type in self.__model.classes()]

        if document_type.value.lower() not in classes:
            raise InvalidDocumentTypeError(
                f"Tipo de documento informado ({document_type.value}) "
                f"não é um tipo válido. Permitidos: {', '.join(classes)}"
            )
