PROMPT_TO_EXTRACT_INFO_FROM_CODE = """Attached you will find a code snippet from a code base. Extract info to keep track of the code's dependencies.
Return the extracted info as triplets for updating a graph. E.g. (subject, predicate, object)
Prefer the available predicates, add a new one if required
------------
Available predicates:
<<AVAILABLE_PREDICATES>>
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
(client, UNKNOWN, UNKNOWN)
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
<<CODE_SNIPPET>>
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
<<CODE_SNIPPET>>
Explanation:
"""