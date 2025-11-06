import json
import os
import warnings
from io import BytesIO
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from keras.models import load_model
from keras.preprocessing import image

from api.src.infra import IMAGE_SIZE, PATH_METRICS, PATH_MODEL
from api.src.infra.logs import logger
from api.src.use_cases.classify_documents.contracts import ModelClassifyDocumentsInterface

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # mostra apenas erros
warnings.filterwarnings("ignore")


class ModelClassifyDocuments(ModelClassifyDocumentsInterface):
    """
    Classe responsável por receber uma imagens e retornar a resposta segundo o modelo
    """

    def __init__(self) -> None:
        try:
            self.model = load_model(PATH_MODEL)
            self._target_size = IMAGE_SIZE
            class_names = self._load_class_names(Path(PATH_METRICS))
            self._classes: List[str] = [class_names[str(i)] for i in range(len(class_names))]
        except Exception as exc:
            raise ValueError("[ModelClassifyDocuments] - arquivo do modelo ou métricas não encontrado") from exc

    def predict(self, image_bytes: bytes) -> Tuple[str, float]:
        """ "
        Realiza a predição da imagem recebida
        """
        logger.info("[ModelClassifyDocuments] - iniciando a predição")
        try:
            img = image.load_img(BytesIO(image_bytes), target_size=self._target_size)
            img_array = image.img_to_array(img)
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            predictions = self.model.predict(img_array)
            confience = round(float(np.max(predictions)), 2)
            label_index = int(np.argmax(predictions))
            label = self._classes[label_index]

            return str(label), confience

        except Exception as err:
            raise ValueError(f"[ModelClassifyDocuments] - erro ao executar a previsão da imagem: {str(err)}") from err

    def _load_class_names(self, path: Path) -> Dict[str, str]:
        """
        Carrega os nomes das classes a partir de um arquivo JSON.
        """
        with open(path, "r", encoding="utf-8") as f:
            metrics_data = json.load(f)

        if "dict_classes" not in metrics_data:
            raise ValueError("A chave 'dict_classes' não foi encontrada no arquivo de métricas.")

        return metrics_data["dict_classes"]  # type: ignore[no-any-return]

    def classes(self) -> List[str]:
        return self._classes
