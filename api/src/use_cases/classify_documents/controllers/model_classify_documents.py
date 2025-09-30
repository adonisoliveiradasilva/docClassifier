from abc import ABC, abstractmethod
from typing import Dict


class ModelCNNInterface(ABC):
    """
    Interface para a classe ClassifyImage
    """
    @abstractmethod
    def model_predict(self, image_bytes: bytes) -> Dict:
        """
        Método responsável por receber uma imagens e retornar a resposta segundo o modelo
        de visão computacional.

        O modelo utilizado no projeto é Convolutional Neural Network (CNN).

        Args:
            image_bytes (bytes): imagem em bytes enviada pelo client

        Returns:
            Dict: dicionário com a resposta do modelo
        """
        raise NotImplementedError("O método model_predict deve ser implementado")
