import networkx as nx
# from modules.vectorgraph.base.types import

class BaseNetworkXGraph:

    def __init__(
            self
        ):
        pass

    def _get_node_by_id(self, node_id):
        return self.graph.nodes[node_id]
    
    def _get_node_by_value(self, value):
        for node in self.graph.nodes:
            if self.graph.nodes[node]["value"] == value:
                return node
        return None
    
    def _get_node_by_type_and_value(self, node_type, value):
        for node in self.graph.nodes:
            if self.graph.nodes[node]["type"] == node_type and self.graph.nodes[node]["value"] == value:
                return node
        return None
    
    def _get_nodes_of_type(self, node_type):
        nodes = []
        for node in self.graph.nodes:
            if self.graph.nodes[node]["type"] == node_type:
                nodes.append(node)
        return nodes
    
    def _get_all_related_node_ids(self, node_id, ignore_nodes=None):
        if ignore_nodes is None:
            ignore_nodes = []
        successors = self.graph.successors(node_id)
        predecessors = self.graph.predecessors(node_id)
        return [node for node in list(successors) + list(predecessors) if node not in ignore_nodes]
    
    def _get_rel_map(self, node_id):
        # get all the relationships of a node
        successors = self.graph.successors(node_id)
        predecessors = self.graph.predecessors(node_id)
        # serialize the relationships
        # each relationship is a tuple (start_node, end_node, relationship_type) with all the data
        rel_map = []
        for successor in successors:
            rel_map.append((self._get_node_by_id(node_id), self._get_node_by_id(successor), self.graph[node_id][successor]))
        for predecessor in predecessors:
            rel_map.append((self._get_node_by_id(predecessor), self._get_node_by_id(node_id), self.graph[predecessor][node_id]))
        return rel_map
    
    def _get_closest_identifier(self, node_id, max_level=3):
        # if nore is an identifier, return it
        if self.graph.nodes[node_id]["type"] == "identifier":
            return node_id, 0
        level = 1
        # ignore the node itself
        ignore_nodes = [node_id]
        # get the first level of successors and predecessors
        rel_nodes = self._get_all_related_node_ids(node_id, ignore_nodes)
        while True:
            # check if there is any identifier
            for _node in rel_nodes:
                if self.graph.nodes[_node]["type"] == "identifier":
                    return _node, level
            # if no identifier was found, check the next level
            if level >= max_level:
                return None, None
            level += 1
            # get the next level of successors and predecessors
            next_rel_nodes = []
            # ignore the nodes already checked
            ignore_nodes.extend(rel_nodes)
            for _node in rel_nodes:
                next_rel_nodes.extend(self._get_all_related_node_ids(_node, ignore_nodes))
            # update the rel_nodes
            rel_nodes = next_rel_nodes
    
    def _get_unique_identifiers_from_nodes(self, nodeids: list[int]) -> list[int]: # insights is a list of node ids of type 'insight'
        # for each insight, get the closest identifier and return it
        identifiers = []
        for nodeid in nodeids:
            identifier, _ = self._get_closest_identifier(nodeid)
            if identifier is not None:
                identifiers.append(identifier)
        return list(set(identifiers))
    
    def _get_closest_chunk_from_identifier(self, identifier, max_level=3):
        """
        Get the closest chunk to an identifier and the level of the relationship:
        Level represents the shortest path between the identifier and the chunk nodes.
        """
        # if it is a chunk, return it
        if self.graph.nodes[identifier]["type"] == "chunk":
            return identifier, 0
        assert self.graph.nodes[identifier]["type"] == "identifier", "The node is not an identifier"
        level = 1 # the level of the relationship, 1 is the closest
        # ignore the node itself
        ignore_nodes = [identifier]
        # get the first level of successors and predecessors
        rel_nodes = self._get_all_related_node_ids(identifier, ignore_nodes)
        while True:
            # check if there is any chunk
            for _node in rel_nodes:
                if self.graph.nodes[_node]["type"] == "chunk":
                    return _node, level
            # if no chunk was found, check the next level
            if level >= max_level:
                return None, None
            level += 1
            # get the next level of successors and predecessors
            next_rel_nodes = []
            # ignore the nodes already checked
            ignore_nodes.extend(rel_nodes)
            for _node in rel_nodes:
                next_rel_nodes.extend(self._get_all_related_node_ids(_node, ignore_nodes))
            # update the rel_nodes
            rel_nodes = next_rel_nodes

    def _get_unique_chunks_from_identifiers(self, identifiers: list[int]) -> list[int]: # identifiers is a list of node ids of type 'identifier'
        # for each identifier, get the closest chunk and return it
        chunks = []
        for identifier in identifiers:
            chunk, _ = self._get_closest_chunk_from_identifier(identifier)
            if chunk is not None:
                chunks.append(chunk)
        return list(set(chunks))