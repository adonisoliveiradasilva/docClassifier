from unittest import mock

import pytest
from fastapi import HTTPException, status

from api.src.main.validators import validate_image


@pytest.mark.asyncio
async def test_validator_image_none(mock_request_form):

    mock_request_form.form.return_value = {}

    with pytest.raises(HTTPException) as info:
        await validate_image(mock_request_form)

    assert info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert info.value.detail == "Imagem não fornecida"


@pytest.mark.asyncio
async def test_validator_image_invalid_type(mock_request_form):

    invalid_file = mock.MagicMock()
    invalid_file.content_type = "application/pdf"
    mock_request_form.form.return_value = {"image": invalid_file}

    with pytest.raises(HTTPException) as info:
        await validate_image(mock_request_form)

    assert info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert info.value.detail == "Arquivo deve ser uma imagem do tipo: PNG, JPEG ou JPG"


@pytest.mark.asyncio
async def test_validator_image_valid(mock_request_form, mock_image_validate):

    mock_request_form.form.return_value = {"image": mock_image_validate}

    image_bytes = await validate_image(mock_request_form)

    assert isinstance(image_bytes, bytes)
    assert len(image_bytes) > 0
    mock_image_validate.read.assert_awaited_once()
