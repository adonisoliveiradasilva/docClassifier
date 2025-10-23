from abc import ABC, abstractmethod
from typing import List, Tuple


class ModelClassifyDocumentsInterface(ABC):
    """
    Interface do modelo para o caso de uso classify_documents
    """

    @abstractmethod
    def predict(self, image_bytes: bytes) -> Tuple[str, float]:
        """
        Método responsável por receber uma imagens e retornar a predição.

        Args:
            image_bytes: imagem em bytes enviada pelo client

        Returns:
            Tuple: (label_da_classe, pontuação_de_confiança)
        """
        raise NotImplementedError("O método predict deve ser implementado")

    @abstractmethod
    def classes(self) -> List[str]:
        """
        Método responsável por retornar as classes do modelo.

        Returns:
            list: lista de classes
        """
        raise NotImplementedError("O método classes deve ser implementado")
