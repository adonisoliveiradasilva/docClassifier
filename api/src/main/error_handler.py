from fastapi import Request, status
from fastapi.responses import JSONResponse

from api.src.infra.logs import logger
from api.src.main.schemas.base import ResponseModel
from api.src.use_cases.classify_documents import InvalidDocumentTypeError, PredictionError


async def invalid_document_type_handler(_request: Request, exc: InvalidDocumentTypeError) -> JSONResponse:
    """Handler para erros de tipo de documento inválido."""
    content = ResponseModel(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message=str(exc),
        data={"error_type": exc.__class__.__name__},
    ).model_dump()

    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content)


async def prediction_error_handler(_request: Request, exc: PredictionError) -> JSONResponse:
    """Handler para erros de predição."""
    logger.error(f"[PredictionError] - Erro não esperado na predição: {exc}")
    content = ResponseModel(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Erro interno no servidor durante a classificação.",
        data={"error_type": exc.__class__.__name__},
    ).model_dump()

    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=content)
