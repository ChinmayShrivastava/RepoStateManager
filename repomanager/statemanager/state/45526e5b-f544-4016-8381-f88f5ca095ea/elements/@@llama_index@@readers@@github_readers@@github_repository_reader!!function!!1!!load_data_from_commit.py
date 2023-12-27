    def load_data_from_commit() -> None:
        """Load data from a commit."""
        documents = reader1.load_data(
            commit_sha="22e198b3b166b5facd2843d6a62ac0db07894a13"
        )
        for document in documents:
            print(document.metadata)
