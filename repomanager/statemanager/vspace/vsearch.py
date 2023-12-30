import json
from typing import List
from ._chromadb import return_collection

with open("../state/running_state.json", "r") as f:
    running_state = json.load(f)
repo_id = running_state["repo_id"]

_path = f"../state/{repo_id}/meta/storage"

class VectorSearch():

    def __init__(self,
            collection_name,
            collection_path = _path,
            n = 5
        ) -> None:

        self.collection_path = collection_path
        self.collection_name = collection_name
        self.collection = return_collection(path=collection_path, collection_name=collection_name)
        self.n = n # number of results to return

    def search(self, query: str, type: str = None) -> List[tuple]:
        """takes in a query and returns a list of tuples of the form (node_name, node_type)"""

        # TODO: make sure type is in the schema (probably perform a fuzzy search on the available types)

        if not type:
            res = self.collection.query(
                query_texts=[query],
                n_results=self.n
            )
        else:
            res = self.collection.query(
                query_texts=[query],
                n_results=self.n,
                where={'type': type}
            )
        metadatas = res['metadatas'][0]
        return [(metadata['name'], metadata['type']) for metadata in metadatas]