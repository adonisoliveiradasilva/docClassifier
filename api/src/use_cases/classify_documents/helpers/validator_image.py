from pathlib import Path
from fastapi import UploadFile
from api.src.domain.response_http import HttpRequestError

allowed_mime_types = ["image/png", "image/jpeg"]
allowed_extensions = [".png", ".jpg", ".jpeg"]

async def image_validator(image: UploadFile) -> bytes:
    """
    Valida se o arquivo enviado é uma imagem do tipo permitido (PNG ou JPEG) e com extensão permitida
    e retorna o bytes da imagem
    """
    print("entrando na validação")
    if not image:
        raise HttpRequestError("Imagem inválida ou ausente", status_code=422)

    # Checa MIME type
    if not image.content_type or image.content_type not in allowed_mime_types:
        raise HttpRequestError(
            f"Arquivo deve ser uma imagem do tipo: {', '.join(allowed_mime_types)}",
            status_code=422
        )

    # Checa extensão
    ext = Path(image.filename).suffix.lower()
    if ext not in allowed_extensions:
        raise HttpRequestError(
            f"Arquivo deve ter extensão: {', '.join(allowed_extensions)}",
            status_code=422
        )
    images_bytes = await image.read()
    if not images_bytes:
        raise HttpRequestError("Imagem inválida ou ausente", status_code=422)

    return images_bytes
