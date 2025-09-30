from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from api.src.use_cases.classify_documents.classify_docs import ClassifyDocuments
from api.src.infra.controllers.classify_documents.model_classify_documents import ModelCNN
from api.src.domain.response_http import HttpRequestError
from api.src.use_cases.classify_documents.helpers import image_validator


predict_image_routes = APIRouter()

# Rota de predição de imagem
@predict_image_routes.post("/prediction")
async def predict(image: UploadFile = File(...)):
    """
    Rota de predição de imagem, a rota recebe uma imagem e retorna a predição da imagem.
    """
    try:
        image_bytes = await image_validator(image)

        classifier  = ClassifyDocuments(ModelCNN())
        prediction = classifier.execute(image=image_bytes)

        return JSONResponse(
            status_code=200,
            content={
                "status": 200,
                "message": "Operação realizada com sucesso",
                "data": prediction
            }
        )

    except HttpRequestError as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "status": e.status_code,
                "message": e.message,
                "data": None
            }
        )
