from typing import Dict
from api.src.domain.use_cases.classify_image import ClassifyImageInterface


class PredictImageController:
    def __init__(self, use_case: ClassifyImageInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: Dict) -> Dict:
        
        image_input = http_request["body"]["image"]
        response = self.__use_case.execute(image_input)
        http_response = {"statusCode": 200, "data": response}

        return http_response
