import json
from typing import List

from keras import backend as K
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.models import Model
from keras.optimizers import Adam
from keras.utils import DirectoryIterator
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from api.ml_training.architecture_model import ArchitectureModel
from api.ml_training.constants import BATCH_SIZE, EPOCHS, LEARNING_RATE, METRICS_NAME, MODEL_NAME, PATH_SALVE_MODEL
from api.ml_training.dataset_loader import ImageDatasetLoader
from api.src.infra.logs import logger


class ModelClassifyDocumentsTrain:
    """
    Classe responsável por iniciar o treinamento do modelo de classificação de documentos.
    """

    def run_train(self) -> None:
        """
        Método responsável por orquestra o pipeline de treinamento.
        """
        logger.info("[ModelClassifyDocumentsTrain] - iniciando o treinamento do modelo")
        try:
            train_gen, val_gen, class_names = ImageDatasetLoader().pre_process_images_train()

            arch_model = ArchitectureModel()
            model = arch_model.model(num_classes=len(class_names))

            model.compile(
                optimizer=Adam(learning_rate=LEARNING_RATE), loss="categorical_crossentropy", metrics=["accuracy"]
            )

            callbacks = [
                EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True),
                ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=3),
            ]

            model.fit(
                train_gen,
                epochs=EPOCHS,
                validation_data=val_gen,
                batch_size=BATCH_SIZE,
                callbacks=callbacks,
                steps_per_epoch=train_gen.n // BATCH_SIZE,
                validation_steps=val_gen.n // BATCH_SIZE,
            )

            self._salve_metrics_model(model, val_gen, class_names)

            model_path = PATH_SALVE_MODEL + MODEL_NAME
            model.save(model_path)
            logger.info(f"[ModelClassifyDocumentsTrain] - modelo salvo em: {model_path}")

        except Exception as err:
            logger.error(f"[ModelClassifyDocumentsTrain] - erro ao treinar o modelo: {str(err)}")
            raise
        finally:
            K.clear_session()

    def _salve_metrics_model(self, model: Model, val_gen: DirectoryIterator, class_names: List[str]) -> None:
        """
        Método responsável por salvar as métricas do modelo treinado.

        Args:
            model: modelo treinado
            val_gen: dados de validação
            class_names: classes do modelo
        """

        logger.info("[ModelClassifyDocumentsTrain] - iniciando avaliação do modelo")
        try:
            y_predicts = model.predict(val_gen)
            y_pred_classes = y_predicts.argmax(axis=1)
            y_true_classes = val_gen.classes

            accurary = accuracy_score(y_true_classes, y_pred_classes)
            report = classification_report(y_true_classes, y_pred_classes, target_names=class_names)
            conf_matrix = confusion_matrix(y_true_classes, y_pred_classes)

            metrics_data = {
                "accuracy": accurary,
                "classification_report": report,
                "confusion_matrix": conf_matrix.tolist(),
                "dict_classes": val_gen.class_indices,
            }

            with open(PATH_SALVE_MODEL + METRICS_NAME, "w", encoding="utf-8") as f:
                json.dump(metrics_data, f, indent=4, ensure_ascii=False)
        except Exception as err:
            logger.error(f"[ModelClassifyDocumentsTrain] - erro ao avaliar e salvar as métricas do modelo: {str(err)}")


# Execução do treinamento
if __name__ == "__main__":
    ModelClassifyDocumentsTrain().run_train()
