import cv2
import numpy as np
from api.src.errors.http_request_error import HttpRequestError
import logging


# pylint: disable=no-member
class ImagePreprocessor:
    """ 
    Classe para pre-processa imagens
    """
    def __init__(self, target_size=(224, 224)):
        self.target_size = target_size

    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Pré-processa uma imagem recebida em bytes para o modelo.
        Args:
            image_bytes (bytes): Imagem em bytes
        Returns:
            np.ndarray: Imagem normalizada e redimensionada

        """
        try:
            logging.info("[preprocess_image]: Iniciando o pré-processamento da imagem")
            if not isinstance(image_bytes, bytes):
                raise HttpRequestError(f"A entrada deve ser bytes, recebido: {type(image_bytes)}", status_code=400)

            image_array = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            if image is None:
                raise HttpRequestError("Não foi possível decodificar a imagem dos bytes fornecidos", status_code=422)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, self.target_size)
            image = image / 255.0
            image = np.expand_dims(image, axis=0)

            return image
        except HttpRequestError:
            raise
        except Exception as e:
            raise HttpRequestError(f"Erro no pré-processamento da imagem: {str(e)}", status_code=422)
