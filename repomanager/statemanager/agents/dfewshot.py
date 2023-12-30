from ..vspace._chromadb import return_collection, add_docs_to_collection

path_ = "toolsfortools/fewshot/storage"
dfs_collection = return_collection(path=path_, collection_name='dynamic_fewshot')

filename = "llama_index"
few_shots_file_path = f"toolsfortools/fewshot/examples/{filename}.txt"

example_delimiter = "|||"

few_show_delimiter = "~~~"

def get_few_shots_list(few_shots_file_path):
    with open(few_shots_file_path, "r") as f:
        few_shots_list = f.read()
    few_shots_list = few_shots_list.split(few_show_delimiter)
    few_shots_list = [few_shots.split(example_delimiter) for few_shots in few_shots_list]
    return few_shots_list

def add_few_shots(few_shots_list, collection):
    docs = [few_shots[0] for few_shots in few_shots_list]
    metadata = [{
        "question": few_shots[1],
        "response": few_shots[2],
        "repo": filename
        } for few_shots in few_shots_list]
    len_ = collection.count()
    ids = [len_+idx for idx in range(len(few_shots_list))]
    add_docs_to_collection(docs, metadata, ids, collection)

few_shots_list = get_few_shots_list(few_shots_file_path)
add_few_shots(few_shots_list, dfs_collection)
print(dfs_collection.count())