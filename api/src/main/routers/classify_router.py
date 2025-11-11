from typing import Optional, Union

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse

from api.src.domain.enums import DocumentTypeEnum
from api.src.main.dependencies import get_model_classifier
from api.src.main.schemas import ClassificationResponseModel, PredictionResponse, ResponseErrorModel, ResponseModel
from api.src.main.validators.validator_image import validate_image
from api.src.use_cases.classify_documents import ClassifyDocuments

router = APIRouter(tags=["ClassifyDocuments"], prefix="/model")


@router.post(
    "/classify_docs",
    response_model=ResponseModel,
    description=(
        "Classifica a imagem enviada (ex: CNH, RG, Passaporte) e valida "
        "se o tipo identificado pelo modelo corresponde ao tipo informado pelo usuário."
    ),
    responses={
        200: {"model": PredictionResponse},
        422: {"model": ResponseModel},
        500: {"model": ResponseErrorModel},
    },
)
async def classify_docs(
    document_type_str: Optional[str] = Form(None, alias="documentType"),
    model_use_case: ClassifyDocuments = Depends(get_model_classifier),
    image_bytes: bytes = Depends(validate_image),
) -> Union[PredictionResponse, JSONResponse]:
    """
    Rota para classificar o documento.

    Se o documento for classificado corretamente, retorna o resultado da classificação.
    """
    if not document_type_str:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Tipo de documento não fornecido.",
        )
    try:
        expected_document_type = DocumentTypeEnum(document_type_str.lower())
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Tipo de documento inválido: {document_type_str}."
        ) from err

    try:
        result = await run_in_threadpool(
            model_use_case.execute,
            image_bytes=image_bytes,
            document_type=expected_document_type,
        )

        payload = ClassificationResponseModel.model_validate(result.__dict__)

        if not payload.is_match:
            error_response = ResponseModel(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                message=f"Não foi possível identificar {document_type_str.upper()} na imagem enviada.",
                data=payload,
            )
            return JSONResponse(status_code=status.HTTP_200_OK, content=error_response.model_dump())

        return PredictionResponse(
            status_code=status.HTTP_200_OK,
            message="Imagem confere com o tipo informado.",
            data=payload,
        )

    except Exception as err:
        error_response = ResponseErrorModel(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Erro interno no servidor durante a classificação",
            data={"error_type": str(err)},
        )
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=error_response.model_dump())
