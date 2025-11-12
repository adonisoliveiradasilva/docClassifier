from unittest import mock

import pytest

from api.src.domain.enums import DocumentTypeEnum
from api.src.use_cases.classify_documents import PredictionError
from api.src.use_cases.classify_documents.classify_documents import ClassifyDocuments, InvalidDocumentTypeError


def test_classify_documents_init(mock_use_case):

    classify_documents = ClassifyDocuments(model_classifier=mock_use_case)
    assert classify_documents is not None


def test_classify_documents_validate_type_input(mock_use_case, mock_image):
    classify_documents = ClassifyDocuments(model_classifier=mock_use_case)

    # cria um tipo inválido (não presente no Enum)
    class FakeDocumentTypeEnum:
        """Cria um tipo inválido para teste."""

        value = "titulo_eleitor"

    document_invalid_test = FakeDocumentTypeEnum()

    with pytest.raises(InvalidDocumentTypeError) as info:
        classify_documents.execute(image_bytes=mock_image, document_type=document_invalid_test)

    assert "Tipo de documento informado (titulo_eleitor)" in str(info.value)
    assert "não é um tipo válido." in str(info.value)


def test_classify_documents_error_predict(mock_use_case, mock_image):

    mock_use_case.classes = mock.MagicMock(return_value=["rg", "cnh", "passaporte"])
    mock_use_case.predict.side_effect = PredictionError("Erro ao fazer a predição")
    classify_documents = ClassifyDocuments(model_classifier=mock_use_case)

    input_document = DocumentTypeEnum.RG

    with pytest.raises(PredictionError) as info:
        classify_documents.execute(image_bytes=mock_image, document_type=input_document)

    assert "[ClassifyDocuments] - falha ao obter predição do modelo - Erro ao fazer a predição" in str(info.value)


def test_classify_documents_diff_label(mock_use_case, mock_image):

    mock_use_case.classes = mock.MagicMock(return_value=["rg", "cnh", "passaporte"])
    input_document = DocumentTypeEnum.RG
    classify_documents = ClassifyDocuments(model_classifier=mock_use_case)

    mock_use_case.predict.return_value = ("conta", 0.60)

    with pytest.raises(PredictionError) as info:
        classify_documents.execute(image_bytes=mock_image, document_type=input_document)

    assert "[ClassifyDocuments] - classe predita desconhecida: conta" in str(info.value)


def test_classify_documents_sucess(mock_use_case, mock_image):

    mock_use_case.classes = mock.MagicMock(return_value=["rg", "cnh", "passaporte"])
    input_document = DocumentTypeEnum.RG
    classify_documents = ClassifyDocuments(model_classifier=mock_use_case)

    mock_use_case.predict.return_value = ("rg", 0.90)

    result = classify_documents.execute(image_bytes=mock_image, document_type=input_document)

    assert result.user_expected_type == DocumentTypeEnum.RG
    assert result.model_predicted_type == DocumentTypeEnum.RG
    assert result.confidence_score == 0.90
    assert result.is_match is True
