# import neo4j driver
from neo4j import GraphDatabase
import tqdm
import threading
import time
from agents.retrievers.graph import get_code
from agents.retrievers.defaults import ELEMENTS_THAT_CONTAIN_CODE
import logging
import os
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.INFO)

# start the driver
driver = GraphDatabase.driver(  
    uri=f"{os.getenv('NEO4J_URL')}",
    auth=(os.getenv('NEO4J_ADMIN'), os.getenv('NEO4J_PASSWORD_DROPLET')),
    )

# KNOWN_EDGE_TYPES = [
#     "dir-to-file", 
#     "imports_directly", 
#     "REQUIRED_TYPE", 
#     "EXTERNAL_DEPENDENCY", 
#     "class", 
#     "function", 
#     "function-call", 
#     "parent_class", 
#     "dir-to-dir",
#     "class-method",
#     "imports_from",
#     "is_a_submodule_of",
#     "root-to-dir",
#     ]

# def migrate(repo_name, G):
#     extra = []
#     for edge in G.edges(data=True):
#         if 'type' in edge[2]:
#             if edge[2]['type'] not in KNOWN_EDGE_TYPES:
#                 extra.append(edge[2]['type'])
#                 continue
#             if edge[2]['type'] == 'root-to-dir':
#                 # create a root node if it doesn't exist
#                 root = RootDirectory.nodes.get_or_none(
#                     name=repo_name,
#                     path='/',
#                     )
#                 if root is None:
#                     root = RootDirectory(
#                         name=repo_name,
#                         path='/',
#                         )
#                 # create a directory node if it doesn't exist
#                 directory = Directory.nodes.get_or_none(
#                     name=edge[1],
#                     root_dir_node_id=root.uid,
#                     )
#                 if directory is None:
#                     directory = Directory(
#                         name=edge[1],
#                         root_dir_node_id=root.uid,
#                         )
#                 # create a relationship between root and directory
#                 root.directories.connect(directory)
#                 # save the directory node
#                 directory.save()
#                 # save the root node
#                 root.save()
#             elif edge[2]['type'] == 'dir-to-dir':
#                 pass
#             elif edge[2]['type'] == 'dir-to-file':
#                 pass
#             elif edge[2]['type'] == 'class':
#                 pass
#             elif edge[2]['type'] == 'function':
#                 pass
#             elif edge[2]['type'] == 'function-call':
#                 pass
#             elif edge[2]['type'] == 'parent_class':
#                 pass
#             elif edge[2]['type'] == 'class-method':
#                 pass
#             elif edge[2]['type'] == 'imports_from':
#                 pass
#             elif edge[2]['type'] == 'imports_directly':
#                 pass
#             elif edge[2]['type'] == 'REQUIRED_TYPE':
#                 pass
#             elif edge[2]['type'] == 'EXTERNAL_DEPENDENCY':
#                 pass
#             elif edge[2]['type'] == 'is_a_submodule_of':
#                 pass
#             else:
#                 pass

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

def migrate(repo_name, repo_id, G):

    nodes = [node for node in G.nodes(data=True)]

    def chunks(lst, n):
        # divides the list into n chunks
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    nodes = list(chunks(nodes, 8000))

    # threads = []
    # for i in range(len(nodes)):
    #     t = threading.Thread(target=migrate_nodes, args=(nodes[i],))
    #     threads.append(t)
    #     t.start()
    #     time.sleep(0.1)
    # for t in threads:
    #     t.join()
            
    # # wait for the threads to finish
            
    # edges = [edge for edge in G.edges(data=True)]

    # edges = list(chunks(edges, 20000))

    # threads = []
    # for i in range(len(edges)):
    #     t = threading.Thread(target=migrate_edges, args=(edges[i],))
    #     threads.append(t)
    #     t.start()
    #     time.sleep(0.1)
    # for t in threads:
    #     t.join()

    # wait for the threads to finish
            
    # add code and explanation where possible
    threads = []
    for i in range(len(nodes)):
        t = threading.Thread(target=add_code, args=(nodes[i], repo_id))
        threads.append(t)
        t.start()
        time.sleep(0.1)
    for t in threads:
        t.join()

    # wait for the threads to finish
        
def add_code(nodes, repo_id):
    for node in tqdm.tqdm(nodes, desc='code and explanation'):
        if 'type' not in node[1]:
            continue
        if node[1]['type'] not in ELEMENTS_THAT_CONTAIN_CODE:
            continue
        print(node)
        # add code if it exists
        type = node[1]['type']
        if type in ELEMENTS_THAT_CONTAIN_CODE:
            node[1]['code'] = get_code(node[1], repo_id, node[1]['elementname'])
        query = ''
        # add the code to the already existing node with name node[0]
        query += "MATCH (n:Node {name: '" + format_text_for_neo4j(node[0]) + "'}) "
        query += "SET n.code = '" + format_text_for_neo4j(node[1]['code']) + "' "
        with driver.session() as session:
            session.run(query)


def migrate_nodes(nodes):
    for node in tqdm.tqdm(nodes, desc='nodes'):
        query = ''
        # add the name of the node
        query += "MERGE (n:Node {name: '" + format_text_for_neo4j(node[0]) + "'}) "
        # add the properties of the node
        for prop in node[1].keys():
            if prop == 'info':
                continue
            query += "SET n." + format_text_for_neo4j(prop) + " = '" + format_text_for_neo4j(str(node[1][prop])) + "' "
        with driver.session() as session:
            session.run(query)

def migrate_edges(edges):
    for edge in tqdm.tqdm(edges, desc='edges'):
        if 'type' not in edge[2]:
            continue
        query = ''
        # add the name of the node
        query += "MATCH (n1:Node {name: '" + format_text_for_neo4j(edge[0]) + "'}) "
        query += "MATCH (n2:Node {name: '" + format_text_for_neo4j(edge[1]) + "'}) "
        query += "MERGE (n1)-[r:RELATIONSHIP {type: '" + format_text_for_neo4j(edge[2]['type']) + "'}]->(n2) "
        # add the properties of the node
        for prop in edge[2].keys():
            if prop == 'type':
                continue
            query += "SET r." + format_text_for_neo4j(prop) + " = '" + format_text_for_neo4j(str(edge[2][prop])) + "' "

        with driver.session() as session:
            session.run(query)

def test_connection():
    with driver.session() as session:
        # print the total number of nodes and the total number of edges
        result = session.run("MATCH (n) RETURN count(n)")
        for record in result:
            print(record)

if __name__ == '__main__':
    test_connection()