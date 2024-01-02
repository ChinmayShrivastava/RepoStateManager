from neomodel import config, StructuredNode, StringProperty, IntegerProperty, UniqueIdProperty, RelationshipTo
from neomodel.contrib import SemiStructuredNode
from neo4j import GraphDatabase
config.DATABASE_URL = 'bolt://neo4j:neo4j@localhost:7687'

class RootDirectory(SemiStructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    # boolean is_file
    is_file = IntegerProperty(default=0)
    path = StringProperty(required=True)
    # create relaionships to directories and files
    directories = RelationshipTo('Directory', 'CONTAINS')
    files = RelationshipTo('File', 'CONTAINS')

class Directory(SemiStructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    # boolean is_file
    is_file = IntegerProperty(default=0)
    root_dir_node_id = StringProperty(required=True)
    # create relaionships to directories and files
    directories = RelationshipTo('Directory', 'CONTAINS')
    files = RelationshipTo('File', 'CONTAINS')

class File(SemiStructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    # boolean is_file
    is_file = IntegerProperty(default=1)
    file_type = StringProperty(required=True)
    file_extension = StringProperty(required=True)
    root_dir_name = StringProperty(required=True)
    content = StringProperty(required=True)
    imports = StringProperty(required=True)
    # create relatioships to elements
    elements = RelationshipTo('Element', 'CONTAINS')

class Element(SemiStructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(required=True)
    # boolean is_file
    is_file = IntegerProperty(default=0)
    root_dir_name = StringProperty(required=True)
    ele_type = StringProperty(required=True)
    props = StringProperty(required=True)