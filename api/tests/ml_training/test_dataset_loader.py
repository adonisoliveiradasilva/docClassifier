from unittest import mock

import pytest

from api.ml_training.dataset_loader import ImageDatasetLoader


class TestImageDataGenerator:
    """
    Testes da classe ImageDatasetLoader
    """

    @pytest.fixture
    def setup(self):
        run = ImageDatasetLoader()
        yield run

    @mock.patch("api.ml_training.dataset_loader.image_dataset_from_directory")
    @mock.patch("api.ml_training.dataset_loader.logger")
    def test_pre_process_images_train_error(self, mock_logger, mock_flow, setup):

        mock_flow.side_effect = Exception("Erro de teste")

        with pytest.raises(Exception):
            setup.pre_process_images_train()

        mock_logger.error.assert_called_once_with(
            "[ImageDatasetLoader] - erro ao processar as imagens para o treinamento: Erro de teste"
        )

    @mock.patch("api.ml_training.dataset_loader.image_dataset_from_directory")
    @mock.patch("api.ml_training.dataset_loader.logger")
    def test_not_classes(self, mock_logger, mock_flow, setup):

        mock_train_gen = mock.MagicMock()
        mock_validation_gen = mock.MagicMock()
        mock_train_img_gen = mock.MagicMock()
        mock_val_img_gen = mock.MagicMock()

        mock_train_img_gen.flow_from_directory.return_value = [mock_train_gen]
        mock_val_img_gen.flow_from_directory.return_value = [mock_validation_gen]
        mock_flow.side_effect = [mock_train_img_gen, mock_val_img_gen]

        mock_train_gen.class_indices = None

        with pytest.raises(ValueError, match="Não foi possível determinar o número de classes"):
            setup.pre_process_images_train()

        mock_logger.error.assert_called()
        mock_logger.error.assert_called_once_with(
            "[ImageDatasetLoader] - erro ao processar as imagens para o treinamento: "
            "Não foi possível determinar o número de classes"
        )

    @mock.patch("api.ml_training.dataset_loader.image_dataset_from_directory")
    def test_pre_process_images_train_sucess(self, mock_flow, setup):

        mock_train_gen = mock.MagicMock()
        mock_validation_gen = mock.MagicMock()
        mock_train_gen.class_names = ["cnh", "rg", "passaporte", "outros"]

        mock_train_gen.map.return_value = mock_train_gen
        mock_train_gen.prefetch.return_value = mock_train_gen
        mock_validation_gen.map.return_value = mock_validation_gen
        mock_validation_gen.prefetch.return_value = mock_validation_gen

        mock_flow.side_effect = [mock_train_gen, mock_validation_gen]

        train_generator, validation_generator, class_labels = setup.pre_process_images_train()

        assert train_generator == mock_train_gen
        assert validation_generator == mock_validation_gen
        assert set(class_labels) == {"cnh", "rg", "passaporte", "outros"}

        assert mock_flow.call_count == 2
