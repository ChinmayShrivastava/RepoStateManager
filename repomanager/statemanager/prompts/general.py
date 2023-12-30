PROMPT_TO_EXTRACT_INFO_FROM_CODE = """Attached you will find a code snippet from a code base. Extract info to keep track of the code's dependencies.
Return the extracted info as triplets for updating a graph. E.g. (subject, predicate, object)
Prefer the available predicates, add a new one if required
------------
Available predicates:
- EXTERNAL_DEPENDENCY
- REQUIRED_TYPE
------------
Example1:
Code snippet:
def add_files(file_names_raw):
    files = []
    for file_name_raw in file_names_raw:
        file = client.files.create(
            file=open(file_name_raw["file_name"], 'rb'),
            purpose='assistants'
            )
        files.append(file.id)
    return files
Code triplets:
(add_files, EXTERNAL_DEPENDENCY, file_names_raw)
(file_names_raw, REQUIRED_TYPE, a dictionary or a type of array of dictionaries with each dictionary item mapping a filename to a string value)
(add_files, EXTERNAL_DEPENDENCY, client)
Example2:
Code snippet:
def extract_education_and_experience(split_files):
    education_experience = []
    for file in split_files:
        split_file = file.split('##')
        education_experience.append(split_file)
    return education_experience
Code triplets:
(extract_education_and_experience, EXTERNAL_DEPENDENCY, split_files)
(split_files, REQUIRED_TYPE, list of strings where each string separates string by the delimiter '##')
------------
Code snippet:
{code}
Code triplets:
"""

PROMPT_TO_EXPLAIN_CODE = """Attached you will find a code snippet from a code base. Explain in very simple and concise terms what the code does.
------------
Example1:
Code snippet:
def add_files(file_names_raw):
    files = []
    for file_name_raw in file_names_raw:
        file = client.files.create(
            file=open(file_name_raw["file_name"], 'rb'),
            purpose='assistants'
            )
        files.append(file.id)
    return files
Explanation:
The function add_files takes in an argument, file_names_raw, which is an iterable containing a list of dictionary elements. It returns an list of file ids, where each file id seems to be representing a object returned by the client.files.create method.
Example2:
Code snippet:
def extract_education_and_experience(split_files):
    education_experience = []
    for file in split_files:
        split_file = file.split('##')
        education_experience.append(split_file)
    return education_experience
Explanation:
The function extract_education_and_experience takes in a list of string elements. Splits each element into two sections by the delimiter "##" which represent education and experience respectively. It then returns a list of lists, where each nested list element contains the education and experience sections respectively.
------------
Code snippet:
{code}
Explanation:
"""

PROMPT_TO_GENERATE_SCHEMA = """Attached you will find some triplets from a information graph of the form (start node, edge type, end node).
The triplets have the same edge type.
Try to come up with a general explanation of the edge type to track the schema.
Do not out put anything but the triplet.
----------
Example:
Triplets:
('root', 'root-to-dir', 'embed.py')
('root', 'root-to-dir', 'chunker.py')
('root', 'root-to-dir', '__init__.py')
('root', 'root-to-dir', 'update_database.py')
('root', 'root-to-dir', 'prompts.py')
('root', 'root-to-dir', 'agents.py')
Schema: (root-directory, root-to-dir, paths in the base code directory)
----------
Example:
Triplets:
('embed.py', 'function', 'embed_pipeline')
('chunker.py', 'function', 'extract_education_and_experience')
('update_database.py', 'function', 'template_upload_pipeline')
('agents.py', 'function', 'create_thread')
('chunker.py', 'function', 'extract_education_and_experience')
Schema: (file name, function, a function definition that the file contains)
----------
Use the examples to output the schema for the input information
Triplets:
{triplets}
Schema:"""

HUMAN_TO_TECH_SUB_QUERY = (
    "Convert the query into sub-queries that will be used to retreive relevant information from a graphstore and a vector store.\n"
    "Also, specify what store to use for each sub-query.\n"
    "Example:\n"
    "---------------\n"
    "Query:\n"
    "{ex1}\n"
    "Sub-queries:\n"
    "{r1}\n"
    "---------------\n"
    "Query:\n"
    "{ex2}\n"
    "Sub-queries:\n"
    "{r2}\n"
    "---------------\n"
    "Below is the query you need to convert:\n"
    "Query:\n"
    "{query}\n"
    "Sub-queries:\n"
)

GRAPH_AGENT_DESCRIPTION_TEMPLATE = (
    "You are a graph navigator.\n"
    "Your goal is to navigate the graph through predecessors and successors to collect information.\n"
    "The information should be sufficient to answer the query:\n"
    "Query:\n"
    "{query}\n"
    "----------------------------------------\n"
    "Use and reuse the tools to navigate the graph.\n"
    "Return \"Success\" when you have collected sufficient information to answer the query.\n"
    "Do not answer anything else.\n"
)