from typing import List, Tuple

import tensorflow as tf
from keras import layers
from keras.utils import image_dataset_from_directory
from tensorflow.data import Dataset

from api.ml_training.constants import BATCH_SIZE, IMAGE_SIZE, PATH_DATASET_TRAIN, SEED, VALIDATION_SPLIT
from api.src.infra.logs import logger


class ImageDatasetLoader:
    """
    Classe responsável por carregar e pré-processar as imagens para o treinamento do modelo ModelClassifyDocuments.
    """

    def pre_process_images_train(self) -> Tuple[Dataset, Dataset, List[str]]:
        """
        Método responsável por processar as imagens para o treinamento.
        """
        try:
            logger.info("[ImageDatasetLoader] - passo: iniciando o processamento das imagens para o treinamento")

            train_data = image_dataset_from_directory(
                directory=PATH_DATASET_TRAIN,
                image_size=IMAGE_SIZE,
                batch_size=BATCH_SIZE,
                label_mode="categorical",
                shuffle=True,
                subset="training",
                seed=SEED,
                validation_split=VALIDATION_SPLIT,
            )

            validation_data = image_dataset_from_directory(
                directory=PATH_DATASET_TRAIN,
                image_size=IMAGE_SIZE,
                batch_size=BATCH_SIZE,
                label_mode="categorical",
                subset="validation",
                seed=SEED,
                validation_split=VALIDATION_SPLIT,
            )

            class_labels = train_data.class_names

            normalization_layer = layers.Rescaling(1.0 / 255)
            data_augmentation = tf.keras.Sequential(  # pylint: disable=no-member
                [
                    layers.RandomRotation(0.05),
                    layers.RandomTranslation(0.1, 0.1),
                    layers.RandomZoom(0.2),
                    layers.RandomShear(0.15),
                ]
            )

            train_data = train_data.map(lambda x, y: (data_augmentation(normalization_layer(x)), y)).prefetch(
                buffer_size=tf.data.AUTOTUNE
            )
            validation_data = validation_data.map(lambda x, y: (normalization_layer(x), y)).prefetch(
                buffer_size=tf.data.AUTOTUNE
            )

            if class_labels is None or len(class_labels) == 0:
                raise ValueError("Não foi possível determinar o número de classes")

            return train_data, validation_data, class_labels
        except Exception as err:
            logger.error(f"[ImageDatasetLoader] - erro ao processar as imagens para o treinamento: {str(err)}")
            raise
