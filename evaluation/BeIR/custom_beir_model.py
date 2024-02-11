from abc import ABC, abstractmethod
from typing import Dict
import torch
import numpy as np
from modules.vectorgraph.VectorGraph import VectorGraph
import tqdm
import logging

# logger = logging.getLogger(__name__)

def cos_sim(a: torch.Tensor, b: torch.Tensor):
    """
    Computes the cosine similarity cos_sim(a[i], b[j]) for all i and j.
    :return: Matrix with res[i][j]  = cos_sim(a[i], b[j])
    """
    if not isinstance(a, torch.Tensor):
        a = torch.tensor(a)

    if not isinstance(b, torch.Tensor):
        b = torch.tensor(b)

    if len(a.shape) == 1:
        a = a.unsqueeze(0)

    if len(b.shape) == 1:
        b = b.unsqueeze(0)

    a_norm = torch.nn.functional.normalize(a, p=2, dim=1)
    b_norm = torch.nn.functional.normalize(b, p=2, dim=1)
    return torch.mm(a_norm, b_norm.transpose(0, 1)) #TODO: this keeps allocating GPU memory

def dot_score(a: torch.Tensor, b: torch.Tensor):
    """
    Computes the dot-product dot_prod(a[i], b[j]) for all i and j.
    :return: Matrix with res[i][j]  = dot_prod(a[i], b[j])
    """
    if not isinstance(a, torch.Tensor):
        a = torch.tensor(a)

    if not isinstance(b, torch.Tensor):
        b = torch.tensor(b)

    if len(a.shape) == 1:
        a = a.unsqueeze(0)

    if len(b.shape) == 1:
        b = b.unsqueeze(0)

    return torch.mm(a, b.transpose(0, 1))

class BaseSearch(ABC):

    @abstractmethod
    def search(self, 
               queries: Dict[str, str], 
               top_k: int, 
               **kwargs) -> Dict[str, Dict[str, float]]:
        pass

class VectorGraphRetrieval(BaseSearch):

    def __init__(
        self, 
        persisting_dir: str,
        **kwargs
    ):
        self.vg = VectorGraph.from_persisting_dir(
            persisting_dir=persisting_dir,
            verbose=False
        )
        self.verbose = kwargs.get("verbose", True)
        self.results = {}

    def search(
        self,
        corpus,
        queries: Dict[str, str], 
        top_k: int,
        score_function: str = "cos_sim",
        **kwargs
    ) -> Dict[str, Dict[str, float]]:
            
        # logger.info("Loading Queries...")
        query_ids = list(queries.keys())
        self.results = {qid: {} for qid in query_ids}
        queries = [queries[qid] for qid in queries]

        # logger.info("Retrieving...")
        #  use tqdm if verbose is True
        if self.verbose:
            for qid, query in tqdm.tqdm(zip(query_ids, queries), total=len(queries)):
                _res = self.vg.query_with_chunk_ids(
                    query=query,
                    top_k=top_k
                )
                for _res_item in _res:
                    self.results[qid][_res_item[0]] = 1
        else:
            for qid, query in zip(query_ids, queries):
                _res = self.vg.query_with_chunk_ids(
                    query=query,
                    top_k=top_k
                )
                for _res_item in _res:
                    self.results[qid][_res_item[0]] = 1

        # logger.info("Done!")

        return self.results