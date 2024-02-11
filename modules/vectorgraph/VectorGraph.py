import networkx as nx
from modules.vectordb.chromadb import return_collection
from modules.prompts.generation.RESPONSES import DEFATLT_QUERY_RESPONSE_FROM_CHUNKS
from .base.BaseNetworkXGraph import BaseNetworkXGraph
from .base.BaseChromadbStore import BaseChromadbStore
from llama_index.llms import OpenAI
import pickle
import logging

class VectorGraph(BaseNetworkXGraph, BaseChromadbStore):

    def __init__(
            self,
            graph: nx.Graph,
            collection,
            llm = OpenAI(model="gpt-3.5-turbo"),
            verbose: bool = True
            ):
        self.graph = graph
        self.collection = collection
        self.llm = llm
        self.verbose = verbose
        if self.verbose:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)

    @classmethod
    def from_persisting_dir(
        cls, 
        persisting_dir: str,
        verbose: bool = True
    ):
        if verbose:
            logging.basicConfig(level=logging.INFO)
            logger = logging.getLogger(__name__)
            logger.info("Loading graph from persisting directory")
        graph = pickle.load(open(persisting_dir+"/connections/graph.pkl", "rb"))
        collection = return_collection(path=persisting_dir+"/indices/", collection_name="insight_engine")
        # log
        if verbose:
            logger.info(f"Graph loaded from {persisting_dir}")
            logger.info(f"Vector index loaded from {persisting_dir}")
        return cls(graph=graph, collection=collection, verbose=verbose)
    
    def __str__(self):
        len_graph_nodes = len(self.graph.nodes)
        len_graph_edges = len(self.graph.edges)
        total_vector_elements = self.collection.count()
        return f"VectorGraph with {len_graph_nodes} nodes and {len_graph_edges} edges.\nTotal vector elements: {total_vector_elements}"
    
    def _query(
        self,
        query,
        top_k: int = 5
    ) -> list[int]:
        _res_insight_ids = self.top_k_ids(query, top_k)
        _identifiers = self._get_unique_identifiers_from_nodes(_res_insight_ids)
        _chunks = self._get_unique_chunks_from_identifiers(_identifiers)
        return _chunks
    
    def query(
        self,
        query,
        top_k: int = 5
    ) -> list[str]:
        chunks = self._query(query, top_k)
        return [self.graph.nodes[chunk]["value"] for chunk in chunks]

    def _generate_response_from_chunks(self, query: str, chunks: list[str]) -> list[str]:
        prompt = DEFATLT_QUERY_RESPONSE_FROM_CHUNKS.format(
            excerpts="\n".join(chunks),
            query=query
        )
        return self.llm.complete(prompt).text
    
    def generate_response(self, query: str, top_k: int = 5) -> list[str]:
        chunks = self.query(query, top_k)
        return self._generate_response_from_chunks(query, chunks)
    
    def _query_with_chunk_ids(
        self, 
        query: str, 
        top_k: int = 5
    ) -> list[list[int, str]]:
        chunks = self._query(query, top_k)
        return [(self.graph.nodes[chunk]['metadata']['chunk_no'], self.graph.nodes[chunk]["value"]) for chunk in chunks]
    
    def query_with_chunk_ids(
        self, 
        query: str, 
        top_k: int = 5
    ) -> list[list[int, str]]:
        return self._query_with_chunk_ids(query, top_k)