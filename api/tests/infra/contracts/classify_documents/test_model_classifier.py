# pylint: disable=protected-access

from unittest import mock

import pytest

from api.src.infra.contracts.classify_documents.model_classify import ModelClassifyDocuments


@mock.patch("api.src.infra.contracts.classify_documents.model_classify.ModelClassifyDocuments._load_class_names")
@mock.patch("api.src.infra.contracts.classify_documents.model_classify.load_model")
def test_model_classify_documents_init(mock_load_model, mock_load_class_names):

    mock_load_model.return_value = mock.MagicMock()
    mock_load_class_names.return_value = {"RG": 0, "CNH": 1}
    model = ModelClassifyDocuments()

    assert model is not None
    assert model._classes == ["RG", "CNH"]


def test_model_classify_document_not_path():

    with pytest.raises(ValueError) as exc_info:
        ModelClassifyDocuments()

    assert "[ModelClassifyDocuments] - arquivo do modelo ou métricas não encontrado" in str(exc_info.value)


@mock.patch("api.src.infra.contracts.classify_documents.model_classify.ModelClassifyDocuments._load_class_names")
@mock.patch("api.src.infra.contracts.classify_documents.model_classify.load_model")
def test_model_classify_documents_predict_error(mock_load_model, mock_load_class_names, test_image_bytes):

    mock_model_instance = mock.MagicMock()
    mock_model_instance.predict.side_effect = Exception("Erro ao fazer a predição")
    mock_load_model.return_value = mock_model_instance
    mock_load_class_names.return_value = {"RG": 0, "CNH": 1}

    model = ModelClassifyDocuments()

    with pytest.raises(ValueError) as exc_info:
        model.predict(test_image_bytes)

    assert "[ModelClassifyDocuments] - erro ao executar a previsão da imagem: Erro ao fazer a predição" in str(
        exc_info.value
    )


@mock.patch("api.src.infra.contracts.classify_documents.model_classify.ModelClassifyDocuments._load_class_names")
@mock.patch("api.src.infra.contracts.classify_documents.model_classify.load_model")
def test_model_classify_documents_predict_success(mock_load_model, mock_load_class_names, test_image_bytes):

    mock_load_model.predict.return_value = ("RG", 0.95)
    mock_load_class_names.return_value = {"RG": 0, "CNH": 1}
    label, confidence = mock_load_model.predict(test_image_bytes)

    assert label == "RG"
    assert confidence == 0.95
