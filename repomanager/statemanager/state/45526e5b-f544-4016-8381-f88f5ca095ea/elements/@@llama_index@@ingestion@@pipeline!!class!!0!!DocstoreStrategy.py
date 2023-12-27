class DocstoreStrategy(str, Enum):
    """Document de-duplication strategy."""

    UPSERTS = "upserts"
    DUPLICATES_ONLY = "duplicates_only"
    UPSERTS_AND_DELETE = "upserts_and_delete"
