from fastapi import HTTPException, UploadFile, status

ALLOWED_MIME_TYPES = ["image/png", "image/jpeg", "image/jpg"]
ALLOWED_EXTENSIONS = [".png", ".jpg", ".jpeg"]
MAX_FILE_SIZE_MB = 5 * 1024 * 1024


async def validate_image(image: UploadFile) -> bytes:
    """
    Valida se o arquivo enviado é uma imagem do tipo permitido (PNG, JPEG ou JPG).
    """
    if not image:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Imagem não fornecida",
        )

    if not image.content_type or image.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Arquivo deve ser uma imagem do tipo: PNG, JPEG ou JPG",
        )

    image_bytes = await image.read()
    if len(image_bytes) > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Imagem muito grande. Limite: {MAX_FILE_SIZE_MB}MB.",
        )

    return image_bytes
