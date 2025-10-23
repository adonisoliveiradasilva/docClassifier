class UseCaseException(Exception):
    """Classe base para exceções de caso de uso."""


class InvalidDocumentTypeError(UseCaseException):
    """Lançada quando o tipo de documento esperado não é válido."""


class PredictionError(UseCaseException):
    """Lançada quando o modelo falha ao fazer uma predição."""
