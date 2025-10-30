from fastapi.testclient import TestClient

from api.src.domain.enums import DocumentTypeEnum
from api.src.main import app
from api.src.use_cases.classify_documents import PredictionError

client = TestClient(app)


def test_classify_documents_success(mock_image, mock_model):
    result = {
        "user_expected_type": DocumentTypeEnum.CNH,
        "model_predicted_type": DocumentTypeEnum.CNH,
        "confidence_score": 0.9,
        "is_match": True,
    }
    mock_model.execute.return_value = result
    form_data = {"documentType": "cnh"}
    files = mock_image

    response = client.post("/model/classify_docs", data=form_data, files=files)

    assert response.status_code == 200
    assert response.json() == {
        "status_code": 200,
        "message": "Classificação realizada com sucesso",
        "data": {
            "user_expected_type": "cnh",
            "model_predicted_type": "cnh",
            "confidence_score": 0.9,
            "is_match": True,
        },
    }


def test_classify_documents_invalid_document_type(mock_image, mock_model):
    form_data = {"documentType": "invalid_type"}
    files = mock_image

    response = client.post("/model/classify_docs", data=form_data, files=files)

    assert response.status_code == 422
    assert response.json() == {"detail": "Tipo de documento inválido: invalid_type."}
    mock_model.execute.assert_not_called()


def test_classify_documents_internal_errors(mock_image, mock_model):

    mock_model.execute.side_effect = PredictionError("Test")
    form_data = {"documentType": "cnh"}
    files = mock_image

    response = client.post("/model/classify_docs", data=form_data, files=files)

    assert response.status_code == 500
    assert response.json() == {
        "status_code": 500,
        "message": "Erro interno no servidor durante a classificação",
        "data": {"error_type": "PredictionError"},
    }
