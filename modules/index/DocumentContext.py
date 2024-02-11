from modules.tables.TextTableReader import TextTableReader
from modules.actions.graph import add_unique_node, get_nodeid_from_nodevalue
from modules.prompts.extraction.EXTRACT import DEFAULT_EXTRACT_UNIQUE_IDENTIFIERS, DEFAULT_EXTRACT_CITATIONS, DEFAULT_EXTRACT_INSIGHTS
from modules.index.dispatch import DEFAULT_DOCUMENT_CONTEXT_DISPATCH, document_context_dependency_check, dispatch_next_step
from modules.vectordb.chromadb import return_collection, add_entries_to_collection
from modules.vectorgraph.VectorGraph import VectorGraph
from .utilities import connect_identifier_node_to_table_root, is_table_name, parse_tuple_string, parse_tuple_list_string, add_unique_identifier_node
import networkx as nx
from llama_index.llms import OpenAI
import logging
import tqdm
import pickle
import datetime
from dotenv import load_dotenv
import os
import json

load_dotenv()

class DocumentContext:

    vector_collection_name = {
        "insights": "insight_engine",
        "chunks": "chunk_engine",
    }

    def __init__(
            self,
            chunks: list = [],
            G: nx.Graph = nx.DiGraph(),
            verbose: bool = True,
            document_name: str = '',
            persist_dir: str = None,
            is_new = True,
        ):
        self.verbose = verbose
        if self.verbose:
            logging.basicConfig(level=logging.INFO)
        else:
            logging.basicConfig(level=logging.ERROR)
        self.llm = OpenAI(max_tokens=512)
        self.persist_dir = persist_dir
        self.graph_dir = f"{self.persist_dir}/connections/"
        self.vector_collection_dir = f"{self.persist_dir}/indices/"
        if is_new:
            self.dispatch = DEFAULT_DOCUMENT_CONTEXT_DISPATCH
            self.chunks = chunks
            self.G = G
            self.document_name = document_name
            self.document_metadata = {}
            if os.path.exists(self.graph_dir):
                pass
            else:
                os.makedirs(self.graph_dir)
            if os.path.exists(self.vector_collection_dir):
                pass
            else:
                os.makedirs(self.vector_collection_dir)
            self.metadata_path = f"{self.persist_dir}/metadata.json"
            self.chunk_path = f"{self.persist_dir}/chunks.json"
            # export chunks into json
            with open(self.chunk_path, "w") as f:
                json.dump(self.chunks, f, indent=4)
            self.failed_citation_addition = []
            self.failed_insight_addition = []
            # save the graph
            with open(f"{self.persist_dir}/connections/graph.pkl", "wb") as f:
                pickle.dump(self.G, f)
            # update the metadata
            self._update_metadata()
            self._save_metadata()
        else:
            # load the graph
            with open(f"{self.persist_dir}/connections/graph.pkl", "rb") as f:
                self.G = pickle.load(f)
            # load the metadata
            with open(f"{self.persist_dir}/metadata.json", "r") as f:
                self.document_metadata = json.load(f)
            self.document_name = self.document_metadata['document_name']
            self.metadata_path = f"{self.persist_dir}/metadata.json"
            self.chunk_path = f"{self.persist_dir}/chunks.json"
            with open(self.chunk_path, "r") as f:
                self.chunks = json.load(f)
            self.failed_citation_addition = self.document_metadata['failed_citation_addition']
            self.failed_insight_addition = self.document_metadata['failed_insight_addition']
            # update dispatch
            self.dispatch = self.document_metadata['dispatch']

    @classmethod
    def from_pdf_path(
            cls,
            pdf_path,
            persist_dir,
            verbose: bool = True,
            is_new = True
        ):
        tr = TextTableReader(
            pdf_path=pdf_path,
            verbose=verbose,
            )
        tr.extract_all_data()
        return cls(
            chunks=tr.chunks,
            G=tr.G,
            verbose=verbose,
            document_name=tr.file_name,
            persist_dir=persist_dir,
            is_new=is_new
            )
    
    @classmethod
    def from_chunks(
            cls,
            chunks,
            persist_dir,
            verbose: bool = True,
            is_new = True
        ):
        return cls(
            chunks=chunks,
            verbose=verbose,
            persist_dir=persist_dir,
            is_new=is_new
        )
    
    @classmethod
    def load_existing(cls, persist_dir, verbose: bool = True):
        return cls(
            verbose=verbose,
            persist_dir=persist_dir,
            is_new=False
        )
    
    def __str__(self) -> str:
        _str = (
            f"DocumentContext with {len(self.chunks)} chunks.\n"
            f"Graph has {len(self.G.nodes)} nodes and {len(self.G.edges)} edges."
            )
        return _str
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def _save_graph(self):
        with open(f"{self.persist_dir}/connections/graph.pkl", "wb") as f:
            pickle.dump(self.G, f)
        return

    def _save_chunks(self):
        with open(f"{self.persist_dir}/chunks.json", "w") as f:
            json.dump(self.chunks, f, indent=4)
        return

    def _save_metadata(self):
        with open(f"{self.persist_dir}/metadata.json", "w") as f:
            json.dump(self.document_metadata, f, indent=4)
        return
    
    def _update_metadata(self):
        self.document_metadata = {
            "document_name": self.document_name,
            "chunks": len(self.chunks),
            "nodes": len(self.G.nodes),
            "edges": len(self.G.edges),
            "dispatch": self.dispatch,
            "failed_citation_addition": self.failed_citation_addition,
            "failed_insight_addition": self.failed_insight_addition,
            "datetime": str(datetime.datetime.now())
        }
        with open(self.metadata_path, "w") as f:
            json.dump(self.document_metadata, f, indent=4)
        return
    
    def update_state(self):
        self._save_graph()
        self._save_chunks()
        self._update_metadata()
        self._save_metadata()
        return
    
    def _get_unique_chunk_identifiers(self, chunk):
        _prompt = DEFAULT_EXTRACT_UNIQUE_IDENTIFIERS.format(text=chunk)
        _response = self.llm.complete(_prompt).text
        # the response is a tuple of the form "(something, something...)", parse it into a tuple
        parsed_tuple = parse_tuple_string(_response)
        return parsed_tuple
    
    def _add_unique_chunk_identifiers_to_graph(self, chunk, identifiers):
        # add chunk to the graph
        self.G, nodeid = add_unique_node(G=self.G, node_type="chunk", node_value=chunk['text'], metadata=chunk['metadata'])
        # add a identifier node for each identifier
        for identifier in identifiers:
            # self.G, identifier_nodeid = add_unique_node(G=self.G, node_type="identifier", node_value=identifier)
            self.G, identifier_nodeid = add_unique_identifier_node(G=self.G, node_type="identifier", node_value=identifier)
            self.G.add_edge(nodeid, identifier_nodeid, type="contains")
            identifier = str(identifier)
            if is_table_name(identifier):
                self.G = connect_identifier_node_to_table_root(self.G, identifier_nodeid)
        return

    def _add_all_unique_identifiers(self):
        document_context_dependency_check('get_unique_identifiers', self.dispatch)
        for chunk_no in tqdm.tqdm(range(len(self.chunks)), desc="Adding unique identifiers"):
            # log
            logging.info(f'Adding unique identifiers for chunk {chunk_no+1} out of {len(self.chunks)}.')
            if 'identifiers' in self.chunks[chunk_no].keys():
                identifiers = self.chunks[chunk_no]['identifiers']
            else:
                chunk = self.chunks[chunk_no]['text']
                identifiers = self._get_unique_chunk_identifiers(chunk)
            # if verbose, print in green
            if self.verbose:
                print(f"\033[92mExtracted Identifiers: {identifiers}\033[00m")
            self.chunks[chunk_no]['identifiers'] = identifiers
            self._save_chunks()
            self._add_unique_chunk_identifiers_to_graph(self.chunks[chunk_no], identifiers)
        # log
        logging.info('Added all unique identifiers.')
        # update the dispatch
        self.dispatch['get_unique_identifiers'] = True
        self.update_state()
        return
    
    def _get_citations(self, chunk):
        _prompt = DEFAULT_EXTRACT_CITATIONS.format(text=chunk)
        _response = self.llm.complete(_prompt).text
        # the response is a tuple of the form "(something, something...)", parse it into a tuple
        parsed_tuple = parse_tuple_list_string(_response)
        return parsed_tuple

    def _add_citations_to_graph(self, chunk_id, citations):
        for tuple in citations:
            if len(tuple) < 2:
                continue
            referee, referred = tuple
            referee = str(referee).lower()
            referred = str(referred).lower()
            # add an edge between the node with value referee and the node with value referred
            referee_nodeid = get_nodeid_from_nodevalue(self.G, referee)
            referred_nodeid = get_nodeid_from_nodevalue(self.G, referred)
            try:
                assert referee_nodeid is not None, f"Node with value {referee} not found in graph."
                assert referred_nodeid is not None, f"Node with value {referred} not found in graph."
            except AssertionError as e:
                if self.verbose:
                    logging.error(e)
                self.failed_citation_addition.append({
                    chunk_id: (referee, referred)
                })
                continue
            self.G.add_edge(referee_nodeid, referred_nodeid, type="cites")
        return

    def _add_all_citations(self):
        document_context_dependency_check('get_citations', self.dispatch)
        for chunk_no in tqdm.tqdm(range(len(self.chunks)), desc="Adding citations"):
            # log
            logging.info(f'Adding citations for chunk {chunk_no+1} out of {len(self.chunks)}.')
            if 'citations' in self.chunks[chunk_no].keys():
                citations = self.chunks[chunk_no]['citations']
            else:
                chunk = self.chunks[chunk_no]['text']
                _citations = self._get_citations(chunk)
                citations = []
                for citation in _citations:
                    if len(citation) > 2:
                        citations.append((citation[0], " ".join(citation[1:])))
                    else:
                        citations.append(citation)
            # if verbose, print in green
            if self.verbose:
                print(f"\033[92mExtracted Citations: {citations}\033[00m")
            self.chunks[chunk_no]['citations'] = citations
            self._save_chunks()
            self._add_citations_to_graph(chunk_id=chunk_no, citations=citations)
        # log
        logging.info('Added all citations.')
        # update the dispatch
        self.dispatch['get_citations'] = True
        self.update_state()
        return
    
    def _generate_insight(self, chunk):
        _prompt = DEFAULT_EXTRACT_INSIGHTS.format(text=chunk)
        _response = self.llm.complete(_prompt).text
        # the response is a tuple of the form "(something, something...)", parse it into a tuple
        parsed_tuple = parse_tuple_list_string(_response)
        return parsed_tuple
    
    def _add_insights_to_graph(self, chunk_id, insights):
        for insight in insights:
            if len(insight) < 2:
                continue
            unique_identifier, insight = insight
            unique_identifier = str(unique_identifier).lower()
            insight = str(insight).lower()
            # get the nodeid for the unique identifier
            unique_identifier_nodeid = get_nodeid_from_nodevalue(self.G, unique_identifier)
            try:
                assert unique_identifier_nodeid is not None, f"Node with value {unique_identifier} not found in graph."
            except AssertionError as e:
                if self.verbose:
                    logging.error(e)
                self.failed_insight_addition.append({
                    chunk_id: (unique_identifier, insight)
                })
                continue
            # add the insight as a node
            self.G, insight_nodeid = add_unique_node(G=self.G, node_type="insight", node_value=insight)
            # add an edge between the unique identifier and the insight
            self.G.add_edge(insight_nodeid, unique_identifier_nodeid, type="insight_from")
        return

    def _generate_insights(self):
        document_context_dependency_check('get_insights', self.dispatch)
        for chunk_no in tqdm.tqdm(range(len(self.chunks)), desc="Adding insights"):
            # log
            logging.info(f'Adding insights for chunk {chunk_no+1} out of {len(self.chunks)}.')
            if 'insights' in self.chunks[chunk_no].keys():
                insights = self.chunks[chunk_no]['insights']
            else:
                chunk = self.chunks[chunk_no]['text']
                _insights = self._generate_insight(chunk)
                insights = []
                for insight in _insights:
                    if len(insight) > 2:
                        insights.append((insight[0], " ".join(insight[1:])))
                    else:
                        insights.append(insight)
            # if verbose, print in green
            if self.verbose:
                print(f"\033[92mExtracted Insights: {insights}\033[00m")
            self.chunks[chunk_no]['insights'] = insights
            self._save_chunks()
            self._add_insights_to_graph(chunk_id=chunk_no, insights=insights)
        # log
        logging.info('Added all insights.')
        # update the dispatch
        self.dispatch['get_insights'] = True
        self.update_state()
        return
    
    def add_vector_index(self):
        document_context_dependency_check('add_vector_index', self.dispatch)
        collection = return_collection(path=self.vector_collection_dir, collection_name=self.vector_collection_name['insights'])
        # add all the nodes to the collection, nodes that are of the type insight
        # get all the nodes that are of the type insight
        insight_nodes = [node for node in self.G.nodes if self.G.nodes[node]['type'] == 'insight']
        # get the node values
        insight_node_values = [self.G.nodes[node]['value'] for node in insight_nodes]
        # get the nodeids
        insight_nodeids = [str(node) for node in insight_nodes]
        # get the metadata
        insight_node_metadata = [
            {
                "id": node,
            } for node in insight_nodeids
        ]
        # add the entries to the collection
        self.collection = add_entries_to_collection(
            docs=insight_node_values,
            metadata=insight_node_metadata,
            ids=insight_nodeids,
            collection=collection
        )
        # log
        logging.info('Added vector index.')
        # update the dispatch
        self.dispatch['add_vector_index'] = True
        self.update_state()
        return
    
    def persist(self):
        document_context_dependency_check('persist', self.dispatch)
        # persist the graph
        with open(f"{self.graph_dir}graph.pkl", "wb") as f:
            pickle.dump(self.G, f)
        # vector is already persisted
        # persist the metadata after updating it
        self.document_metadata = {
            "document_name": self.document_name,
            "chunks": len(self.chunks),
            "nodes": len(self.G.nodes),
            "edges": len(self.G.edges),
            "dispatch": self.dispatch,
            "failed_citation_addition": self.failed_citation_addition,
            "failed_insight_addition": self.failed_insight_addition,
            "datetime": str(datetime.datetime.now())
        }
        with open(self.metadata_path, "w") as f:
            json.dump(self.document_metadata, f, indent=4)
        # update the dispatch
        self.dispatch['persist'] = True
        self.update_state()
        return
    
    def _generate_document_context(self):
        self._add_all_unique_identifiers()
        self._add_all_citations()
        self._generate_insights()
        self.add_vector_index()
        # log
        logging.info('Document context generation complete. Saving...')
        self.persist()
        logging.info(f'Document context saved in {self.persist_dir}/{self.document_name}.')
        return
    
    def continue_generation(self):
        while True:
            dispatch_next_step(self, self.dispatch)
            if all(self.dispatch.values()):
                break
        return
    
    def as_vector_graph(self):
        # generate the document context
        self.continue_generation()
        # return a VectorGraph object
        return VectorGraph.from_persisting_dir(persisting_dir=self.persist_dir)