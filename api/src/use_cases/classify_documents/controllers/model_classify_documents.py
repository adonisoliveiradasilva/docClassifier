from abc import ABC, abstractmethod
from typing import Dict

import numpy as np


class ModelCNNInterface(ABC):
    """
    Interface do modelo para o caso de uso classify_documents
    """

    classes: list[str]

    @abstractmethod
    def model_predict(self, image_bytes: np.ndarray) -> Dict | None:
        """
        Método responsável por receber uma imagens e retornar a resposta segundo o modelo
        de visão computacional.

        O modelo utilizado no projeto é Convolutional Neural Network (CNN).

        Args:
            image_bytes: imagem em bytes enviada pelo client

        Returns:
            Dict: dicionário com a resposta do modelo
        """
        raise NotImplementedError("O método model_predict deve ser implementado")
