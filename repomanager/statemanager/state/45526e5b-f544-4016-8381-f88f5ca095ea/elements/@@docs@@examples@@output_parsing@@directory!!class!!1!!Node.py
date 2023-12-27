class Node(BaseModel):
    """
    Class representing a single node in a filesystem. Can be either a file or a folder.
    Note that a file cannot have children, but a folder can.

    Args:
        name (str): The name of the node.
        children (List[Node]): The list of child nodes (if any).
        node_type (NodeType): The type of the node, either a file or a folder.

    """

    name: str = Field(..., description="Name of the folder")
    children: List["Node"] = Field(
        default_factory=list,
        description=(
            "List of children nodes, only applicable for folders, files cannot"
            " have children"
        ),
    )
    node_type: NodeType = Field(
        default=NodeType.FILE,
        description=(
            "Either a file or folder, use the name to determine which it"
            " could be"
        ),
    )
