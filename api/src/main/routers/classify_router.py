from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.concurrency import run_in_threadpool

from api.src.domain.enums import DocumentTypeEnum
from api.src.main.dependencies import get_model_classifier
from api.src.main.schemas import (
    ClassificationResponseModel,
    PredictionResponse,
    ResponseBadRequest,
    ResponseErrorModel,
    ResponseModel,
)
from api.src.main.validators.validator_image import validate_image
from api.src.use_cases.classify_documents import ClassifyDocuments

router = APIRouter(tags=["ClassifyDocuments"], prefix="/model")


@router.post(
    "/classify_docs",
    description=(
        "Classifica a imagem enviada (ex: CNH, RG, Passaporte) e valida "
        "se o tipo identificado pelo modelo corresponde ao tipo informado pelo usuário."
    ),
    responses={
        400: {"model": ResponseBadRequest},
        413: {"model": ResponseModel},
        422: {"model": ResponseModel},
        500: {"model": ResponseErrorModel},
    },
)
async def classify_docs(
    document_type_str: str = Form(..., alias="documentType"),
    image: UploadFile = File(...),  # pylint: disable=unused-argument
    model_use_case: ClassifyDocuments = Depends(get_model_classifier),
    image_bytes: bytes = Depends(validate_image),
) -> ResponseModel:
    """
    Rota para classificar o documento.

    Se o documento for classificado corretamente, retorna o resultado da classificação.
    """
    try:
        expected_document_type = DocumentTypeEnum(document_type_str.lower())
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Tipo de documento inválido: {document_type_str}."
        ) from err

    result = await run_in_threadpool(
        model_use_case.execute,
        image_bytes=image_bytes,
        document_type=expected_document_type,
    )

    payload = ClassificationResponseModel.model_validate(result)
    return PredictionResponse(
        status_code=status.HTTP_200_OK, message="Classificação realizada com sucesso", data=payload
    )
    # except Exception as err:
    #     return ResponseErrorModel(
    #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         message="Erro interno no servidor durante a classificação",
    #         data={"error_type": str(err)}
    #     )
