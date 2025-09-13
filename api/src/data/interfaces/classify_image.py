from abc import ABC, abstractmethod
from typing import Dict

class ModelPredictInterface(ABC):
    """
    Interface para a classe ClassifyImage
    """
    @abstractmethod
    def predict(self, image_bytes: bytes) -> Dict:
        pass
