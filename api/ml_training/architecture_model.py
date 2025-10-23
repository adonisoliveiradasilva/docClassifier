from Keras import layers, models
from keras.models import Model

from api.ml_training.constants import INPUT_SHAPE
from api.src.infra.logs import logger


class ArchitectureModel:
    """
    Classe responsável por definir a arquitetura do modelo de classificação de documentos.
    """

    def model(self, num_classes: int) -> Model:
        """
        Método responsável por construir a arquitetura.
        """
        logger.info("[ArchitectureModel] - Construindo a arquitetura do modelo")

        model = models.Sequential(
            [
                layers.Conv2D(32, (3, 3), padding="same", input_shape=INPUT_SHAPE),
                layers.BatchNormalization(),
                layers.Activation("relu"),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Conv2D(64, (3, 3), padding="same"),
                layers.BatchNormalization(),
                layers.Activation("relu"),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Conv2D(128, (3, 3), padding="same"),
                layers.BatchNormalization(),
                layers.Activation("relu"),
                layers.MaxPooling2D(pool_size=(2, 2)),
                layers.Flatten(),
                layers.Dense(256, padding="same"),
                layers.BatchNormalization(),
                layers.Activation("relu"),
                layers.Dropout(0.3),
                layers.Dense(128, padding="same"),
                layers.Activation("relu"),
                layers.Dense(num_classes, activation="softmax"),
            ]
        )

        return model
