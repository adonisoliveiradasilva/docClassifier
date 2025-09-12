from api.src.domain.use_cases.classify_image import ClassifyImageInterface
from api.src.data.interfaces.classify_image import ModelPredictInterface
from typing import Dict

class ClassifyImage(ClassifyImageInterface):
    """ ClassifyImage usecase"""

    def __init__(self, model: ModelPredictInterface) -> None:
        self.__model = model

    def execute(self, image_bytes: bytes) -> Dict:
        response = self.__model.predict(image_bytes)
        return response
