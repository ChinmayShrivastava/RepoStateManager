from pydantic import BaseModel, Field
import networkx as nx

class ReturnedNode(BaseModel):
    name: str
    metadata: dict = Field(default_factory=dict)

class ReturnedEdge(BaseModel):
    start_node: str
    end_node: str
    metadata: dict = Field(default_factory=dict)

class ReturnedEdges(BaseModel):
    edges: list[ReturnedEdge] = Field(default_factory=list)

class ReturnedNodes(BaseModel):
    nodes: list[ReturnedNode] = Field(default_factory=list)