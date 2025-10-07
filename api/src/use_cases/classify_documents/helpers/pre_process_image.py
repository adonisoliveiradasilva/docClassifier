from io import BytesIO
from typing import Tuple

import numpy as np
from tensorflow.keras.preprocessing import image

from api.src.infra.logs import logger


def pre_process_image(image_bytes: bytes, target_size: Tuple[int, int] = (128, 128)) -> np.ndarray:
    """
    Pré-processa uma iamgem para ser usada no modelo

    Args:
        image: imagem enviada pelo client
        target_size: Tamanho para redimensionar a imagem. Default (128, 128)

    Returns:
        np.ndarray: array com shape (1, altura, largura, canais), pronto para entrada no modelo
    """
    logger.info("[pre_process_image]: Iniciando o pré-processamento da imagem")
    try:
        if not isinstance(image_bytes, bytes):
            logger.error("[pre_process_image] - passo: a imagem não é em bytes")
            raise ValueError("A imagem deve ser fornecida em formato bytes")

        img = image.load_img(BytesIO(image_bytes), target_size=target_size)
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array
    except Exception as err:
        logger.error(f"[pre_process_image] - passo: erro ao executar o pré-processamento da imagem: {str(err)}")
        raise
