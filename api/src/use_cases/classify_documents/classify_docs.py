from typing import Dict

from api.src.infra.logs import logger
from api.src.use_cases.classify_documents.controllers import ModelCNNInterface
from api.src.use_cases.classify_documents.helpers import pre_process_image


class ClassifyDocuments:
    """
    Classe responsável por orquestrar as funções de classificação de imagens.
    """

    logger.info("[ClassifyDocuments] - passo: iniciando a classificação de imagens")

    def __init__(self, model: ModelCNNInterface) -> None:
        self.__model = model

    def execute(self, image: bytes) -> Dict:
        """
        Método responsável por orquestrar as funções de classificação de imagens e
        retornar o resultado da classificação.
        """
        try:
            logger.info("[ClassifyDocuments] - passo: iniciando a classificação da imagem")

            # image_bytes = image_validator(image)
            image_array = pre_process_image(image)
            predict = self.__model.model_predict(image_array)
            return predict
        except Exception as err:
            logger.error(f"[ClassifyDocuments] - passo: erro ao executar a classificação da imagem: {str(err)}")
            raise

    def close(self):
        """
        Método para fechar a classificação de imagens.
        """
        self.__model.close()
        logger.info("[ClassifyDocuments] - passo: finalizando a classificação de imagens")
