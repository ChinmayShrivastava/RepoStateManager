class NodeType(str, enum.Enum):
    """Enumeration representing the types of nodes in a filesystem."""

    FILE = "file"
    FOLDER = "folder"
