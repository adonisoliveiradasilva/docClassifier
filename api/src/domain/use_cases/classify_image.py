from abc import ABC, abstractmethod
from typing import Dict, Union


class ClassifyImageInterface(ABC):
    """
    Interface para a classe ClassifyImage
    """
    @abstractmethod
    def execute(self, image_input: Union[str, bytes, object]) -> Dict:
        pass
