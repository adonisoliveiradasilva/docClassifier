import io
from unittest import mock

import pytest

from api.src.main import app
from api.src.main.dependencies import get_model_classifier
from api.src.use_cases.classify_documents.classify_documents import ClassifyDocuments


@pytest.fixture(scope="session")
def image_bytes() -> bytes:
    """
    Carrega uma imagem de teste real do disco.
    """
    try:
        with open("./api/tests/fixtures/cnh.png", "rb") as f:
            return f.read()
    except FileNotFoundError:
        pytest.fail("Imagem de teste 'tests/fixtures/cnh.png' não encontrada.")
        return None


@pytest.fixture
def mock_image(image_bytes):
    """
    Cria um mock de arquivo de imagem para upload.
    """
    return {"image": ("test.png", io.BytesIO(image_bytes), "image/png")}


@pytest.fixture
def mock_image_validate():
    """
    Cria um mock de arquivo de imagem para upload.
    """
    fake_bytes = b"fake image data"
    mock_file = mock.MagicMock()
    mock_file.read = mock.AsyncMock(return_value=fake_bytes)
    mock_file.filename = "test.png"
    mock_file.content_type = "image/png"
    return mock_file


@pytest.fixture
def mock_model():
    """
    Cria um mock para o caso de uso.
    """
    mock_case = mock.MagicMock(spec=ClassifyDocuments)
    app.dependency_overrides[get_model_classifier] = lambda: mock_case
    yield mock_case
    app.dependency_overrides.pop(get_model_classifier, None)


@pytest.fixture
def mock_use_case():
    """
    Cria um mock para o modelo classificador (que possui o método 'predict' e a lista 'classes').
    """
    mock_model_predict = mock.MagicMock()
    mock_model_predict.predict = mock.MagicMock()
    mock_model_predict.classes = ["cnh", "rg", "passaporte"]
    return mock_model_predict


@pytest.fixture
def mock_request_form():
    """
    Cria um mock para o Request com form vazio.
    """
    mock_request = mock.MagicMock()
    mock_request.form = mock.AsyncMock(return_value={})
    return mock_request
