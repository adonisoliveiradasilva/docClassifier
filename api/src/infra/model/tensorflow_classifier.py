import tensorflow as tf
import numpy as np
from api.src.data.interfaces.classify_image import ModelPredictInterface
from api.src.infra.model.image_preprocessor import ImagePreprocessor

# pylint: disable=no-member
# pylint: disable=reportAttributeAccessIssue

class TensorflowImageClassifier(ModelPredictInterface):
    """
    Classe para classificação de imagens com Tensorflow
    """
    def __init__(self):
        model_path = "api/src/infra/model/docsclassifier_model.keras"
        self.model = tf.keras.models.load_model(model_path)
        print(f"Modelo carregado: {self.model}")

        self.classes = ["CNH"]

    def predict(self, image_bytes: bytes) -> dict:
        """
        Faz a predição de uma imagem recebida em bytes.
        Args:
            image_bytes (bytes): Imagem em bytes
        Returns:
            dict: Resultado da predição
        """
        try:
            # Pré-processamento da imagem
            image_array = ImagePreprocessor().preprocess_image(image_bytes)

            # Previsão
            predictions = self.model.predict(image_array)
            predictions = predictions[0]
            predicted_index = int(np.argmax(predictions))
            predicted_class = self.classes[predicted_index]
            confidence = float(predictions[predicted_index])

            # Confiança por classe
            all_confidences = {cls: float(predictions[i]) for i, cls in enumerate(self.classes)}

            return {
                "predicted_class": predicted_class,
                "confidence": confidence,
                "all_confidences": all_confidences
            }

        except Exception:
            return {
                "error": "Não foi possível identificar um documento na imagem",
                "all_confidences": {cls: None for cls in self.classes}
            }

    def close(self):
        if hasattr(self, 'model'):
            self.model.close()