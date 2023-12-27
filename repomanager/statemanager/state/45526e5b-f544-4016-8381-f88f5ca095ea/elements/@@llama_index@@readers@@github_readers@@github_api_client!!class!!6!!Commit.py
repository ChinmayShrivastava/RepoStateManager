    class Commit(DataClassJsonMixin):
        """Dataclass for the commit object in the commit. (commit.commit)."""

        @dataclass
        class Tree(DataClassJsonMixin):
            """
            Dataclass for the tree object in the commit.

            Attributes:
                - sha (str): SHA for the commit
            """

            sha: str

        tree: Tree
