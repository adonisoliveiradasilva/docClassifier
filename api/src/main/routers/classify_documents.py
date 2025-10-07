from typing import Any

from fastapi import APIRouter, File, Form, UploadFile

from api.src.domain.response_http import (
    ResponseBadRequest,
    ResponseErrorModel,
    ResponseHTTP422,
    ResponseWithPredictionDocs,
)
from api.src.infra.controllers.classify_documents.model_classify_documents import ModelCNN
from api.src.infra.logs import logger
from api.src.use_cases.classify_documents.classify_docs import ClassifyDocuments
from api.src.use_cases.classify_documents.helpers import image_validator

from ..response_handler import ResponseHTTPHandler

router = APIRouter(tags=["ClassifyDocuments"], prefix="/model")


@router.post(
    "/model_classify_docs",
    description=(
        "Classifica a imagem enviada (ex: CNH, RG, Passaporte) e valida "
        "se o tipo identificado pelo modelo corresponde ao tipo informado pelo usuário."
    ),
    responses={
        200: {"model": ResponseWithPredictionDocs},
        500: {"model": ResponseErrorModel},
        400: {"model": ResponseBadRequest},
    },
)
def model_classify_docs(documentType: str = Form(...), file: UploadFile = File(...)) -> Any:
    """
    Rota para classificar o documento.

    Se o documento for classificado corretamente, retorna o resultado da classificação.
    """
    try:
        image_bytes = image_validator(file)
        if not isinstance(image_bytes, bytes):
            return ResponseHTTP422(message=image_bytes).response(data={})

        classifier = ClassifyDocuments(ModelCNN())
        data = classifier.execute(image=image_bytes)

        predicted = data["data"]["predicted_class"]
        if predicted.lower() != documentType.lower():
            return ResponseHTTP422(
                message=f"Documento informado ({documentType}) não corresponde ao classificado ({predicted})."
            ).response(data={})

        return ResponseHTTPHandler.create(**data, message="Imagem classificada com sucesso")

    except Exception as err:
        logger.error(f"[model_classify_docs] - erro ao executar a classificação da imagem: {str(err)}")
        return ResponseHTTPHandler.create(status_code=500, data={})
