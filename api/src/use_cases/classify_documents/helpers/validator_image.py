from pathlib import Path
from typing import Union

from fastapi import UploadFile

from api.src.infra.logs import logger

allowed_mime_types = ["image/png", "image/jpeg"]
allowed_extensions = [".png", ".jpg", ".jpeg"]


def image_validator(image: UploadFile) -> Union[bytes, str]:
    """
    Valida se o arquivo enviado é uma imagem do tipo permitido (PNG ou JPEG) e com extensão permitida
    e retorna o bytes da imagem
    """
    logger.info("[image_validator] - execução método image_validator")
    try:
        if not image:
            return "imagem ausente"

        if not image.content_type or image.content_type not in allowed_mime_types:
            return f"Arquivo deve ser uma imagem do tipo: {', '.join(allowed_mime_types)}"

        if not image.filename:
            return "O arquivo enviado não possui um nome válido"

        ext = Path(image.filename).suffix.lower()
        if ext not in allowed_extensions:
            return f"Arquivo deve ser uma imagem do tipo: {', '.join(allowed_mime_types)}"

        images_bytes = image.file.read()
        if not images_bytes:
            logger.info("[image_validator] - erro ao converter imagem para bytes")

        return images_bytes

    except Exception as err:
        logger.error(f"[image_validator] - erro na execução método image_validator: {str(err)}")
        return "Erro ao converter imagem para bytes"
