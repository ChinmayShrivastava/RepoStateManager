        class Tree(DataClassJsonMixin):
            """
            Dataclass for the tree object in the commit.

            Attributes:
                - sha (str): SHA for the commit
            """

            sha: str
