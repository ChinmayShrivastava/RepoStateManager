class IndexManagement(int, enum.Enum):
    """Enumeration representing the supported index management operations."""

    NO_VALIDATION = auto()
    VALIDATE_INDEX = auto()
    CREATE_IF_NOT_EXISTS = auto()
