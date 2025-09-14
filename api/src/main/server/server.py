from fastapi import FastAPI
from api.src.main.routes.predict_image import predict_image_routes
from fastapi.middleware.cors import CORSMiddleware

# Aplicação FastAPI
app = FastAPI(
    title="API Docs Classifier",
    description="API para classificação de documentos usando TensorFlow.",
    version="1.0.0",
    debug=True
)

app.include_router(predict_image_routes, prefix="/api", tags=["prediction"])

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # libera só essas origens
    allow_credentials=True,
    allow_methods=["*"],           # libera todos os métodos (POST, GET, etc)
    allow_headers=["*"],           # libera todos os headers
)
