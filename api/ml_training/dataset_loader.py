from typing import List, Tuple

from tensorflow.keras.preprocessing.image import DirectoryIterator, ImageDataGenerator

from api.ml_training.constants import BATCH_SIZE, IMAGE_SIZE, PATH_DATASET_TRAIN, SEED, VALIDATION_SPLIT
from api.src.infra.logs import logger


class ImageDatasetLoader:
    """
    Classe responsável por carregar e pré-processar as imagens para o treinamento do modelo ModelClassifyDocuments.
    """

    def pre_process_images_train(self) -> Tuple[DirectoryIterator, DirectoryIterator, List[str]]:
        """
        Método responsável por processar as imagens para o treinamento.
        """
        try:
            logger.info("[ImageDatasetLoader] - passo: iniciando o processamento das imagens para o treinamento")
            train_datagen = ImageDataGenerator(
                rescale=1.0 / 255,
                rotation_range=15,
                width_shift_range=0.1,
                height_shift_range=0.1,
                shear_range=0.15,
                zoom_range=0.2,
                fill_mode="nearest",
                validation_split=VALIDATION_SPLIT,
            )
            train_generator = train_datagen.flow_from_directory(
                directory=PATH_DATASET_TRAIN,
                target_size=IMAGE_SIZE,
                batch_size=BATCH_SIZE,
                class_mode="categorical",
                shuffle=True,
                subset="training",
                seed=SEED,
            )

            validation_datagen = ImageDataGenerator(rescale=1.0 / 255, validation_split=VALIDATION_SPLIT)
            validation_generator = validation_datagen.flow_from_directory(
                directory=PATH_DATASET_TRAIN,
                target_size=IMAGE_SIZE,
                batch_size=BATCH_SIZE,
                class_mode="categorical",
                shuffle=False,
                subset="validation",
                seed=SEED,
            )
            class_labels = list(train_generator.class_indices.keys())

            if class_labels is None or len(class_labels) == 0:
                raise ValueError("Não foi possível determinar o número de classes")

            return train_generator, validation_generator, class_labels
        except Exception as err:
            logger.error(f"[ImageDatasetLoader] - erro ao processar as imagens para o treinamento: {str(err)}")
            raise
