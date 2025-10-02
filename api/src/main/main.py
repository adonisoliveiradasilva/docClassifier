import pkgutil
import importlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.src.infra.logs import logger


# Aplicação FastAPI
app = FastAPI(
    title="API Docs Classifier",
    description="API para classificação de documentos usando TensorFlow.",
    version="1.0.0",
    debug=True,
    docs_url=None,
    redoc_url="/documentation",
)


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


def import_routers(directory: str) -> None:
    """
    Método que importa as rotas do projeto de forma dinâmica.

    Args:
        directory: caminho do módulo onde as rotas a serem importadas estão.
    """
    for _, module_name, _ in pkgutil.iter_modules([directory]):
        try:
            module = importlib.import_module(f"{directory.replace('/', '.')}.{module_name}")
            if hasattr(module, "__path__"):
                import_routers(f"{directory}/{module_name}")
            else:
                app.include_router(module.router)
        except Exception as err:
            logger.error(f"[import_routers] - erro ao executar a classificação da imagem: {str(err)}")

import_routers("api/src/main/routers")
