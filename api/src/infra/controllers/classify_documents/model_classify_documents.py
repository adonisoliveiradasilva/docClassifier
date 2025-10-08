import os
import warnings
from typing import Dict

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
from tensorflow.keras import backend as K
from tensorflow.keras.models import load_model

from api.src.infra.logs import logger
from api.src.use_cases.classify_documents.controllers import ModelCNNInterface

warnings.filterwarnings("ignore")


class ModelCNN(ModelCNNInterface):
    """
    Classe responsável por receber uma imagens e retornar a resposta segundo o modelo
    """

    def __init__(self) -> None:
        self.path_model = "api/src/infra/models/model_classify_documents/model_cnn.h5"
        self.classes = ["cng", "rg", "passaport"]
        self.model_cnn = load_model(self.path_model)
        if self.model_cnn is None:
            raise ValueError("Erro ao carregar o modelo CNN")

    def model_predict(self, image_bytes: bytes) -> Dict:
        logger.info("[ModelCNN] - passo: iniciando a previsão da imagem")
        try:
            predict = self.model_cnn.predict(image_bytes)
            if predict is None:
                logger.error("[ModelCNN] - passo: erro ao executar a previsão da imagem")
                raise ValueError

            predict = predict[0]
            predicted_index = int(np.argmax(predict))
            predicted_class = self.classes[predicted_index]
            confidence = float(predict[predicted_index])
            all_confidences = {cls: float(predict[i]) for i, cls in enumerate(self.classes)}

            return {
                "status_code": 200,
                "data": {
                    "predicted_class": predicted_class,
                    "confidence": confidence,
                    "all_confidences": all_confidences,
                },
            }

        except Exception as err:
            logger.error(f"[ModelCNN] - passo: erro ao executar a previsão da imagem: {str(err)}")
            return None
            # "Não foi possível identificar um documento na imagem"

        finally:
            K.clear_session()
