from typing import Dict
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
import numpy as np


from api.src.use_cases.classify_documents.controllers import ModelCNNInterface
from api.src.infra.logs import logger

import warnings
warnings.filterwarnings("ignore")


class ModelCNN(ModelCNNInterface):
    """
    Classe responsável por receber uma imagens e retornar a resposta segundo o modelo
    """

    def __init__(self) -> None:
        self.path_model = "api/models/model_cnn.h5"
        self.classes = ["cng", "rg", "passaport"]


    def model_predict(self, image_bytes: bytes) -> Dict:
        logger.info(
            "[ModelCNN] - passo: iniciando a previsão da imagem"
        )
        model_cnn = None
        try:
            model_cnn = load_model(self.path_model)
            if model_cnn is None:
                logger.error("[ModelCNN] - passo: erro ao carregar o modelo")
                raise ValueError

            predict = model_cnn.predict(image_bytes)
            if predict is None:
                logger.error("[ModelCNN] - passo: erro ao executar a previsão da imagem")
                raise ValueError
            
            predict = predict[0]
            predicted_index = int(np.argmax(predict))
            predicted_class = self.classes[predicted_index]
            confidence = float(predict[predicted_index])
            all_confidences = {cls: float(predict[i]) for i, cls in enumerate(self.classes)}

            return {
                "status": 200,
                "message": "Operação realizada com sucesso",
                "predicted_class": predicted_class,
                "confidence": confidence,
                "all_confidences": all_confidences
            }
        
        except Exception as err:
            logger.error(f"[ModelCNN] - passo: erro ao executar a previsão da imagem: {str(err)}")
            return {
                "status": 500,
                "message": f"Erro ao executar a previsão da imagem: {str(err)}"
                # "Não foi possível identificar um documento na imagem"
            }

        finally:
            if model_cnn is not None:
                del model_cnn
                K.clear_session()
