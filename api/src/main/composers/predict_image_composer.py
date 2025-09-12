from api.src.infra.model.tensorflow_classifier import TensorflowImageClassifier
from api.src.data.use_cases.classify_image import ClassifyImage
from api.src.presentation.controllers.predict_image_controller import PredictImageController


def predict_image_composer():
    """
    Cria e compõe o controller de predição de imagens.
    """
    infra= TensorflowImageClassifier()
    use_case = ClassifyImage(infra)
    controller = PredictImageController(use_case)

    return controller
