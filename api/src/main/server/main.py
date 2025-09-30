from fastapi import FastAPI
from api.src.main.routes.classify_documents import predict_image_routes
from fastapi.middleware.cors import CORSMiddleware

# Aplicação FastAPI
app = FastAPI(
    title="API Docs Classifier",
    description="API para classificação de documentos usando TensorFlow.",
    version="1.0.0",
    debug=True,
    docs_url=None,
    redoc_url="/documentation",
)

app.include_router(predict_image_routes, prefix="/api", tags=["prediction"])

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)