import networkx as nx
from modules.vectordb.chromadb import return_collection
import pickle
import logging

class VectorGraph:

    def __init__(
            self,
            graph: nx.Graph,
            collection,
            verbose: bool = True
            ):
        self.graph = graph
        self.collection = collection
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
        logger.info(f"Graph loaded from {persisting_dir}")
        logger.info(f"Vector index loaded from {persisting_dir}")
        return cls(graph, collection, verbose)
