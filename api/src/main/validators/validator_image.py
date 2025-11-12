from typing import Union

from fastapi import HTTPException, Request, status
from starlette.datastructures import UploadFile

ALLOWED_MIME_TYPES = ["image/png", "image/jpeg", "image/jpg"]
ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg"]


async def validate_image(request: Request) -> bytes:
    """
    Valida se o arquivo enviado é uma imagem do tipo permitido (PNG, JPEG ou JPG).
    """
    form = await request.form()
    image: Union[UploadFile, str, None] = form.get("image")

    if not image or not hasattr(image, "read") or not hasattr(image, "content_type"):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Imagem não fornecida ou formato inválido",
        )

    if not image.content_type or image.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Arquivo deve ser uma imagem do tipo: PNG, JPEG ou JPG",
        )

    image_bytes = await image.read()

    return image_bytes
