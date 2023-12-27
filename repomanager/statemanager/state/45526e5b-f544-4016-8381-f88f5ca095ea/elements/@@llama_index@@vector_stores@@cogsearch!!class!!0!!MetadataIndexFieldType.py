class MetadataIndexFieldType(int, enum.Enum):
    """
    Enumeration representing the supported types for metadata fields in an
    Azure Cognitive Search Index, corresponds with types supported in a flat
    metadata dictionary.
    """

    STRING = auto()  # "Edm.String"
    BOOLEAN = auto()  # "Edm.Boolean"
    INT32 = auto()  # "Edm.Int32"
    INT64 = auto()  # "Edm.Int64"
    DOUBLE = auto()  # "Edm.Double"
