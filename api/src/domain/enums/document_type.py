from enum import Enum


class DocumentTypeEnum(str, Enum):
    """
    Tipos de documentos aceitos pelo modelo para classificação.
    """

    CNH = "cnh"
    RG = "rg"
    PASSAPORTE = "passaporte"
    OUTROS = "outros"
