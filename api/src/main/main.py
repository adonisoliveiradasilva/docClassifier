# mypy: disable-error-code=arg-type
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.src.main.error_handler import invalid_document_type_handler, prediction_error_handler
from api.src.main.routers import classify_router
from api.src.use_cases.classify_documents.exceptions import InvalidDocumentTypeError, PredictionError


def create_app() -> FastAPI:
    """
    Função responsável por criar a instância do FastAPI e configurar middlewares, rotas e handlers de erro.
    """
    fastapi_app = FastAPI(
        title="API Docs Classifier",
        description="API para classificação de documentos usando TensorFlow e Clean Architecture.",
        version="1.0.0",
        docs_url="/swagger",
        redoc_url="/docs",
    )

    # Middlewares - CORS)
    origins = [
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ]
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    fastapi_app.add_exception_handler(InvalidDocumentTypeError, invalid_document_type_handler)
    fastapi_app.add_exception_handler(PredictionError, prediction_error_handler)

    fastapi_app.include_router(classify_router.router)

    return fastapi_app


app = create_app()
