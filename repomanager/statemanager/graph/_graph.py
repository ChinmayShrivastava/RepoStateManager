from abc import abstractclassmethod, abstractmethod, ABC

from statemanager.graph.type import ReturnedEdges
from .type import *
from typing import Optional
import pickle
import logging
from statemanager.agents.retrievers.graph import get_code, ELEMENTS_THAT_CONTAIN_CODE, get_method_code, get_class_code
import networkx as nx
from neo4j import GraphDatabase
import time

# ELEMENTS_THAT_CONTAIN_CODE = ['class']

def format_text_for_neo4j(text):
    text = text.replace("\\", "\\\\")
    text = text.replace("'", "\\'")
    text = text.replace('"', '\\"')
    text = text.replace("\n", "\\n")
    text = text.replace("\r", "\\r")
    text = text.replace("\t", "\\t")
    text = text.replace("\b", "\\b")
    text = text.replace("\f", "\\f")
    return text

class Graph(ABC):
    """
    Abstract Graph class
    """
    def __init__(self):
        pass

    @abstractmethod
    def add_node(self, node) -> None:
        pass

    @abstractmethod
    def add_edge(self, edge) -> None:
        pass

    @abstractmethod
    def get_node_metadata(self, node_name) -> dict:
        pass

    @abstractmethod
    def get_edge(self, edge) -> ReturnedEdge:
        pass

    @abstractmethod
    def get_nodes(self) -> ReturnedNodes:
        pass

    @abstractmethod
    def get_edges(self) -> ReturnedEdges:
        pass

    @abstractmethod
    def get_adjacent_edges(self, node) -> ReturnedEdges:
        pass

    @abstractmethod
    def save(self) -> None:
        pass

    @abstractmethod
    def get_code(self, node_metadata, elementname) -> str:
        pass

class NetworkXGraph(Graph):
    """
    NetworkX Graph class
    """
    def __init__(
        self,
        repo_id: Optional[str] = None,
        name: Optional[str] = None,
        path: Optional[str] = None,
        G: Optional[nx.Graph] = None,
        ):
        super().__init__()
        self.repo_id = repo_id
        self.name = name
        self.path = path
        self.G = G if G is not None else None

    @classmethod
    def from_G(
        cls,
        repo_id: str, # required to get code
        G: nx.Graph, # required to save the graph
        ) -> Graph:
        return cls(repo_id=repo_id, G=G)

    @classmethod
    def from_path(
        cls, 
        path: str, # required to save the graph
        ) -> Graph:
        # load the graph from the path
        G = pickle.load(open(path, "rb"))
        return cls(path=path, G=G)

    def add_node(self, node) -> None:
        # if node is not in G, add it
        if node not in self.G.nodes:
            self.G.add_node(node)

    def add_edge(self, edge) -> None:
        # if edge is not in G, add it
        if edge not in self.G.edges:
            self.G.add_edge(edge)

    def get_node_metadata(self, node_name) -> dict:
        return self.G.nodes[node_name]

    def get_edge(self, edge) -> ReturnedEdge:
        pass

    def get_edges(self) -> ReturnedEdges:
        pass

    def get_nodes(self) -> ReturnedNodes:
        pass

    def get_adjacent_edges(self, node) -> ReturnedEdges:
        return ReturnedEdges(edges=self.G.edges(node, data=True))

    def save(self) -> None:
        # if path is none, log an error
        if self.path is None:
            logging.error("**Path is not specified**")
            logging.error(">===Graph not saved===<")
            return
        # save the graph into the path
        pickle.dump(self.G, open(self.path, "wb"))

    def get_code(self, node_metadata, elementname) -> str:
        # if repo_id is none, log an error
        if self.repo_id is None:
            logging.error("**Repo ID is not specified**")
            logging.error(">===Code not retrieved===<")
            return
        return get_code(node_metadata, self.repo_id, elementname)
    
    def get_edges_by_type(self, node_metadata) -> ReturnedEdges:
        if node_metadata['type'] == 'class':
            methods_direct = []
            methods_indirect = []
            parent_class = set()
            for edge in self.G.edges(node_metadata['name'], data=True):
                if edge[2]['type'] == 'class-method':
                    methods_direct.append(ReturnedEdge(start_node=edge[0], end_node=edge[1], metadata=edge[2]))
                elif edge[2]['type'] == 'parent_class':
                    parent_class.add(edge[1])
            for parent in parent_class:
                for edge in self.G.edges(parent, data=True):
                    if edge[2]['type'] == 'class-method':
                        methods_indirect.append(ReturnedEdge(start_node=edge[0], end_node=edge[1], metadata=edge[2]))
            methods = methods_direct
            methods.extend(methods_indirect)
            return ReturnedEdges(edges=methods)
        else:
            # return all edges
            return ReturnedEdges(edges=self.G.edges(node_metadata['name'], data=True))
    
class Neo4JGraph(Graph):

    def __init__(
        self,
        url: Optional[str] = None,
        auth: Optional[tuple[str, str]] = None,
        driver: Optional[GraphDatabase.driver] = None,
        ):
        super().__init__()
        self.url = url
        self.auth = auth
        self.driver = GraphDatabase.driver(uri=url, auth=auth)

    @classmethod
    def from_driver(
        cls,
        driver: GraphDatabase.driver,
        ) -> Graph:
        return cls(driver=driver)
    
    @classmethod
    def from_url(
        cls,
        url: str,
        auth: tuple[str, str],
        ) -> Graph:
        return cls(url=url, auth=auth)
    
    def add_node(self, node) -> None:
        pass

    def add_edge(self, edge) -> None:
        pass

    def get_node_metadata(self, node_name) -> dict:
        with self.driver.session() as session:
            result = session.run(f"MATCH (n) WHERE n.name = '{format_text_for_neo4j(node_name)}' RETURN n")
            single = result.single()[0]
            return {
                item: single[item]
                for item in single
            }
            
    def get_edge(self, edge) -> ReturnedEdge:
        pass

    def get_nodes(self) -> ReturnedNodes:
        pass

    def get_edges(self) -> ReturnedEdges:
        pass

    def get_adjacent_edges(self, node) -> ReturnedEdges:
        query = f"MATCH (n)-[r]-(m) WHERE n.name = '{format_text_for_neo4j(node)}' RETURN n, r, m"
        edges = []
        with self.driver.session() as session:
            result = session.run(query)
            for record in result:
                startnode = record['n']['name']
                endnode = record['m']['name']
                metadata = {
                    item: record['r'][item]
                    for item in record['r']
                }
                edges.append(ReturnedEdge(start_node=startnode, end_node=endnode, metadata=metadata))
        return ReturnedEdges(edges=edges)

    def save(self) -> None:
        pass

    def get_code(self, node_metadata, elementname) -> str:
        if node_metadata['type'] not in ELEMENTS_THAT_CONTAIN_CODE+['method']:
            return 'Sorry, code is not available for this node type.'
        query = f"MATCH (n) WHERE n.elementname = '{format_text_for_neo4j(elementname)}' RETURN n"
        with self.driver.session() as session:
            result = session.run(query)
            single = result.single()[0]
            code = single['code']
        if node_metadata['type'] == 'method':
            code = get_method_code(node_metadata['name'], code)
        elif node_metadata['type'] == 'class':
            code = get_class_code('', code)
        return code
        
    def get_edges_by_type(self, node_metadata) -> ReturnedEdges:
        if node_metadata['type'] == 'class':
            query1 = (
                f"MATCH (n1)-[r1]-(m1) WHERE n1.name = '{format_text_for_neo4j(node_metadata['name'])}' AND r1.type = 'class-method' RETURN n1, r1, m1"
                )
            query2 = (
                f"MATCH (n)-[r]->(m)-[r2]->(o) WHERE n.name = '{format_text_for_neo4j(node_metadata['name'])}' AND r.type = 'parent_class' AND r2.type = 'class-method' RETURN n, r, m, r2, o"
                )
            with self.driver.session() as session:
                result1 = session.run(query1)
                result2 = session.run(query2)
                methods_direct = []
                for record in result1:
                    startnode = record['n1']['name']
                    endnode = record['m1']['name']
                    metadata = {
                        item: record['r1'][item]
                        for item in record['r1']
                    }
                    methods_direct.append(ReturnedEdge(start_node=startnode, end_node=endnode, metadata=metadata))
                methods_indirect = []
                for record in result2:
                    startnode = record['m']['name']
                    endnode = record['o']['name']
                    metadata = {
                        item: record['r2'][item]
                        for item in record['r2'].keys()
                    }
                    methods_indirect.append(ReturnedEdge(start_node=startnode, end_node=endnode, metadata=metadata))
                parent_class = set()
                for record in result2:
                    parent_class.add(record['m']['name'])
                methods = methods_direct
                methods.extend(methods_indirect)
                return ReturnedEdges(edges=methods)
        else:
            # return all edges
            query = f"MATCH (n)-[r]-(m) WHERE n.name = '{format_text_for_neo4j(node_metadata['name'])}' RETURN n, r, m"
            with self.driver.session() as session:
                result = session.run(query)
                methods = []
                for record in result:
                    startnode = record['n']['name']
                    endnode = record['m']['name']
                    metadata = {
                        item: record['r'][item]
                        for item in record['r']
                    }
                    methods.append(ReturnedEdge(start_node=startnode, end_node=endnode, metadata=metadata))
                return ReturnedEdges(edges=methods)