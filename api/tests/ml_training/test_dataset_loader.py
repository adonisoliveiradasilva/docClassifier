from unittest import mock

import pytest

from api.ml_training.dataset_loader import ImageDatasetLoader


@mock.patch("api.ml_training.dataset_loader.ImageDataGenerator.flow_from_directory")
def test_pre_process_images_train(mock_flow):

    mock_train_gen = mock.MagicMock()
    mock_validation_gen = mock.MagicMock()
    mock_train_gen.class_indices = {"cnh": 0, "rg": 1, "passaporte": 2, "outros": 3}

    mock_flow.side_effect = [mock_train_gen, mock_validation_gen]

    loader = ImageDatasetLoader()
    train_generator, validation_generator, class_labels = loader.pre_process_images_train()

    assert train_generator == mock_train_gen
    assert validation_generator == mock_validation_gen
    assert set(class_labels) == {"cnh", "rg", "passaporte", "outros"}

    assert mock_flow.call_count == 2


@mock.patch("api.ml_training.dataset_loader.logger")
@mock.patch("api.ml_training.dataset_loader.ImageDataGenerator.flow_from_directory")
def test_pre_process_images_train_exception(mock_flow, mock_logger):

    mock_flow.side_effect = Exception("Erro de teste")

    loader = ImageDatasetLoader()
    with pytest.raises(Exception):
        loader.pre_process_images_train()

    mock_logger.error.assert_called_once()
    mock_logger.error.assert_called_with(
        "[ImageDatasetLoader] - erro ao processar as imagens para o treinamento: Erro de teste"
    )
