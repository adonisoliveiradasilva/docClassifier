# pylint: disable=protected-access

from unittest import mock

import pytest

from api.src.infra.contracts.classify_documents.model_classify import ModelClassifyDocuments


@mock.patch("api.src.infra.contracts.classify_documents.model_classify.load_model")
def test_model_classify_documents_init(mock_load_model, mock_use_case):

    mock_load_model.return_value = mock_use_case
    model = ModelClassifyDocuments()

    assert model is not None
    assert model._classes == ["cnh", "outros", "passaporte", "rg"]


@mock.patch("api.src.infra.contracts.classify_documents.model_classify.load_model")
def test_model_classify_document_not_path_model(mock_load_model):

    mock_load_model.side_effect = FileNotFoundError("modelo não encontrado")

    with pytest.raises(ValueError) as exc_info:
        ModelClassifyDocuments()

    assert "[ModelClassifyDocuments] - arquivo do modelo ou métricas não encontrado" in str(exc_info.value)


@mock.patch("api.src.infra.contracts.classify_documents.model_classify.ModelClassifyDocuments._load_class_names")
@mock.patch("api.src.infra.contracts.classify_documents.model_classify.load_model")
def test_model_classify_document_not_path_metrics(mock_load_model, mock_metrics, mock_use_case):

    mock_load_model.return_value = mock_use_case
    mock_metrics.side_effect = FileNotFoundError("métricas não encontradas")

    with pytest.raises(ValueError) as exc_info:
        ModelClassifyDocuments()

    assert "[ModelClassifyDocuments] - arquivo do modelo ou métricas não encontrado" in str(exc_info.value)


@mock.patch("api.src.infra.contracts.classify_documents.model_classify.load_model")
def test_model_classify_documents_predict_error(mock_load_model, mock_use_case, image_bytes):

    mock_load_model.return_value = mock_use_case
    mock_use_case.predict.side_effect = Exception("Erro ao fazer a predição")
    model = ModelClassifyDocuments()

    with pytest.raises(ValueError) as exc_info:
        model.predict(image_bytes)

    assert "[ModelClassifyDocuments] - erro ao executar a previsão da imagem: Erro ao fazer a predição" in str(
        exc_info.value
    )
    mock_use_case.predict.assert_called_once()


def test_model_classify_documents_predict_success(mock_use_case, image_bytes):

    mock_use_case.predict.return_value = ("RG", 0.95)
    label, confidence = mock_use_case.predict(image_bytes)

    assert label == "RG"
    assert confidence == 0.95
