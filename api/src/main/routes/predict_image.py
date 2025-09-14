from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import JSONResponse

from api.src.validators.predict_validator import predict_image_validator
from api.src.errors.http_request_error import HttpRequestError
from api.src.main.adpaters.request_adapter import request_adapter
from api.src.main.composers.predict_image_composer import predict_image_composer
from api.src.errors.log_and_handler_exception import log_and_handle_exception

predict_image_routes = APIRouter()

# Rota de predição de imagem
@predict_image_routes.post("/prediction")
async def predict(request: Request):
    """
    Rota de predição de imagem, a rota recebe uma imagem e retorna a predição da imagem.
    """
    try:
        # Validação da imagem
        form = await request.form()
        image: UploadFile = form.get("file")  # type: ignore
        await predict_image_validator(image)
        
        controller = predict_image_composer()
        
        # Ler o conteúdo da imagem e cria o request
        image_content = await image.read()
        http_request = {
            "body": {
                "image": image_content,
                "filename": image.filename,
                "content_type": image.content_type
            }
        }
        response = await request_adapter(http_request, controller.handle)

        if response is None:
            raise HttpRequestError("Resposta vazia", status_code=500)

    except HttpRequestError as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "status": e.status_code,
                "message": e.message,
                "data": None
            }
        )

    except Exception as e:  # pylint: disable=broad-exception-caught
        response = log_and_handle_exception(e)
        return JSONResponse(
            status_code=response["statusCode"],
            content={
                "status": response["statusCode"],
                "message": "Erro interno no servidor",
                "data": None
            }
        )

    return JSONResponse(
    status_code=response["statusCode"],
    content={
        "status": response["statusCode"],
        "message": response.get("message", "Operação realizada com sucesso"),
        "data": response["data"]
    }
)
