from fastapi import FastAPI
from api.src.main.routes.predict_image import predict_image_routes

# Aplicação FastAPI
app = FastAPI(
    title="API Docs Classifier",
    description="API para classificação de documentos usando TensorFlow.",
    version="1.0.0",
    debug=True
)

app.include_router(predict_image_routes, prefix="/api", tags=["prediction"])
