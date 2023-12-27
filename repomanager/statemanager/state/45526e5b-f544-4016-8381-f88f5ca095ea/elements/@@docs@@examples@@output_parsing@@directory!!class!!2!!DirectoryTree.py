class DirectoryTree(BaseModel):
    """
    Container class representing a directory tree.

    Args:
        root (Node): The root node of the tree.

    """

    root: Node = Field(..., description="Root folder of the directory tree")
