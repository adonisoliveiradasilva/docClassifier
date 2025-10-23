from functools import lru_cache

from fastapi import Depends

from api.src.infra.contracts.classify_documents import ModelClassifyDocuments
from api.src.use_cases.classify_documents import ClassifyDocuments
from api.src.use_cases.classify_documents.contracts import ModelClassifyDocumentsInterface


@lru_cache(maxsize=1)
def model_classifier() -> ModelClassifyDocumentsInterface:
    """
    O @lru_cache garante que o KerasModelClassifier (e o modelo .h5)
    seja carregado APENAS UMA VEZ na memória, na primeira requisição
    """
    print("Criando instância de KerasModelClassifier...")
    return ModelClassifyDocuments()


def get_model_classifier(
    model_instance: ModelClassifyDocumentsInterface = Depends(model_classifier),
) -> ClassifyDocuments:
    """
    Constrói o caso de uso, injetando a implementação
    concreta do modelo que o FastAPI resolveu.
    """
    return ClassifyDocuments(model_classifier=model_instance)
