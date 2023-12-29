import json
from typing import List

with open("../state/running_state.json", "r") as f:
    running_state = json.load(f)
repo_id = running_state["repo_id"]

class VectorSearch():

    def __init__(self) -> None:
        pass

    def search(self, query: str, type: str = None) -> List[tuple]:
        """takes in a query and returns a list of tuples of the form (node_name, node_type)"""
        pass