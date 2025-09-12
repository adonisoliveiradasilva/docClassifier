from pathlib import Path
from api.src.errors.http_request_error import HttpRequestError


allowed_mime_types = ["image/png", "image/jpeg"]
allowed_extensions = [ ".png", ".jpg", ".jpeg"]
async def predict_image_validator(image):
    """
    Valida se o arquivo enviado é uma imagem do tipo permitido (PNG ou JPEG).
    """
    try:
        if image is None or image == "":
            raise HttpRequestError("Imagem inválida ou ausente", status_code=422)

        # Checa o MIME type
        if not image.content_type or image.content_type not in allowed_mime_types:
            raise HttpRequestError(
                f"Arquivo dever ser uma imagem do tipo: {', '.join(allowed_mime_types)}",
                status_code=422
            )
        # Checa a extensão
        ext = Path(image.filename).suffix.lower()
        if ext not in allowed_extensions:
            raise HttpRequestError(
                f"Arquivo deve ter extensão: {', '.join(allowed_extensions)}",
                status_code=422
            )

    except HttpRequestError:
        raise
    except Exception as e:
        raise HttpRequestError(f"Erro interno: {str(e)}", status_code=500)
