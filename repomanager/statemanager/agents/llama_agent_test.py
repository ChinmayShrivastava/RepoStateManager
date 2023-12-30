from llama_agents.FunctionCaller import FunctionManager
from llama_agents.tools import tools

if __name__ == "__main__":
    func_agent = FunctionManager.from_tools(
        tools=tools,
        verbose=True,
        max_function_calls=3
    )
    last_tuple = None
    # while True:
    r = func_agent.chat("""Understand the classes implemented better and answer why the error was raised, and provide a solution:
node_postprocessors =[ PrevNextNodePostprocessor(docstore=storage_context.docstore,num_nodes=2,mode="both")]
raise ValueError(f"doc_id \{doc_id\} not found.")
ValueError: doc_id e4e59a11-a8d6-4141-b775-9b60d8af1788 not found.""")
    print(r)
        # print(r)
        # input()