    class Commit(DataClassJsonMixin):
        """Dataclass for the commit object in the branch. (commit.commit)."""

        @dataclass
        class Commit(DataClassJsonMixin):
            """Dataclass for the commit object in the commit. (commit.commit.tree)."""

            @dataclass
            class Tree(DataClassJsonMixin):
                """
                Dataclass for the tree object in the commit.

                Usage: commit.commit.tree.sha
                """

                sha: str

            tree: Tree

        commit: Commit
