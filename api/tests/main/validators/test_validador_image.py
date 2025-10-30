import pytest
from fastapi import HTTPException, status

from api.src.main.validators import ALLOWED_MIME_TYPES, MAX_FILE_SIZE_MB, validate_image


@pytest.mark.asyncio
async def test_validator_image_none():

    with pytest.raises(HTTPException) as info:
        await validate_image(None)

    assert info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert info.value.detail == "Imagem não fornecida"


@pytest.mark.asyncio
async def test_validator_image_invalid_type(mock_upload_file_factory):

    mocked_file = mock_upload_file_factory(content_type="application/pdf", file_size=100)

    with pytest.raises(HTTPException) as info:
        await validate_image(mocked_file)

    assert info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert info.value.detail == "Arquivo deve ser uma imagem do tipo: PNG, JPEG ou JPG"


@pytest.mark.asyncio
async def test_validator_image_too_large(mock_upload_file_factory):

    mocked_file = mock_upload_file_factory(content_type=ALLOWED_MIME_TYPES[0], file_size=MAX_FILE_SIZE_MB + 1)

    with pytest.raises(HTTPException) as info:
        await validate_image(image=mocked_file)

    assert info.value.status_code == status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    assert info.value.detail == f"Imagem muito grande. Limite: {MAX_FILE_SIZE_MB}MB."


@pytest.mark.asyncio
async def test_validator_image_valid(mock_upload_file_factory):

    mocked_file = mock_upload_file_factory(content_type=ALLOWED_MIME_TYPES[0], file_size=1024)

    image_bytes = await validate_image(image=mocked_file)

    assert isinstance(image_bytes, bytes)
    assert len(image_bytes) == 1024
