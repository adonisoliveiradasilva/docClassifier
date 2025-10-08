from typing import Dict

from api.src.infra.logs import logger
from api.src.use_cases.classify_documents.controllers import ModelCNNInterface
from api.src.use_cases.classify_documents.helpers import pre_process_image


class ClassifyDocuments:
    """
    Classe responsável por orquestrar as funções de classificação dos documentos.
    """

    def __init__(self, model: ModelCNNInterface) -> None:
        self.__model = model

    def execute(self, image: bytes, documentType: str) -> Dict:
        """
        Método responsável por orquestrar as funções de classificação de imagens e
        retornar o resultado da classificação.
        """
        logger.info("[ClassifyDocuments] - passo: iniciando a classificação da imagem")
        try:
            self.__validate_document_type_input(documentType)

            image_array = pre_process_image(image)
            predict = self.__model.model_predict(image_array)
            if predict is None:
                return {"message": "Erro interno ao classificar o documento.", "status_code": 500}

            predicted_class = predict["data"]["predicted_class"]

            return self.__compare_types(documentType, predicted_class)

        except Exception as err:
            logger.error(f"[ClassifyDocuments] - passo: erro ao executar a classificação da imagem: {str(err)}")
            return {"message": "Erro interno ao classificar o documento.", "status_code": 500}

    def __validate_document_type_input(self, document_type: str) -> Dict | None:
        """
        Valida se o tipo de documento informado pelo usuário é permitido pelo modelo.
        """
        if document_type.lower() not in map(str.lower, self.__model.classes):
            return {
                "message": (
                    f"Tipo de documento informado ({document_type}) não corresponde aos tipos permitidos: "
                    f"{', '.join(self.__model.classes)}"
                ),
                "status_code": 422,
            }
        return None

    def __compare_types(self, documentType: str, predicted_class: str) -> Dict:
        """
        Método responsável por validar o tipo de documento informado pelo usuário.
        """
        documentType = documentType.lower()
        predicted_class = predicted_class.lower()

        if predicted_class != documentType:
            return {
                "message": f"Documento informado ({documentType}) não corresponde ao classificado ({predicted_class}).",
                "status_code": 422,
            }
        else:
            return {
                "message": f"Documento informado ({documentType}) corresponde ao classificado ({predicted_class}).",
                "status_code": 200,
            }
