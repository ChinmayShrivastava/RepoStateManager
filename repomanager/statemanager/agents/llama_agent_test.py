from llama_agents.FunctionCaller import FunctionManager, AGENT_DESCRIPTION
from llama_agents.tools import tools as _tools
from llama_agents.tools import return_info
from llama_index.llms.openai import OpenAI
from llama_index.types import ChatMessage
import asyncio

# async def func_caller():
#     func_agent = FunctionManager.from_tools(
#         tools=_tools,
#         verbose=True,
#         max_function_calls=5,
#         llm=OpenAI('gpt-4'),
#     )
#     while True:
#         _input = input("Enter a query: ")
#         r = await func_agent.astream_chat(_input)
#         async for token in r.async_response_gen():
#             print(token)


if __name__ == "__main__":
    func_agent = FunctionManager.from_tools(
        tools=_tools,
        verbose=True,
        max_function_calls=5,
        llm=OpenAI('gpt-4'),
    )
    r = func_agent.chat("""Get the code to the init method of the open ai agent class""")
    print(r)
    # last_tuple = None
    # streaming_response = await func_agent.astream_chat("""How would I use async_chat in the agentrunner class and how would I call teh function and return the output?""",
    # chat_history=func_agent.chat_history)
    # print(type(streaming_response))
    # print(type(r))
    # print(streaming_response)


    # for token in streaming_response.response_gen:
    #     print(token)
                                                
    # while True:
    #     _input = input("Enter a query: ")
    #     r = func_agent.chat(_input)
    #     print(r)

    # call the function caller agent
    # asyncio.run(func_caller())

# (venv) (base) chinmayshrivastava@BL-lindsay-C02VP03JJ9JR agents % python llama_agent_test.py
# Added user message to memory: How are SYS ptompts being accessed in teh llamacpp class?
# INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
# === Calling Function ===
# Calling function: semantic_node_finder with args: {
# "query": "SYS prompts in llamacpp class"
# }
# INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
# INFO:httpx:HTTP Request: POST https://api.openai.com/v1/embeddings "HTTP/1.1 200 OK"
# Got output: Find the top five nodes that match the query:
# Query: SYS prompts in llamacpp class
# -------------------
# node name: patch_llmpredictor_predict type: function
# node name: LLMPredictor type: class
# node name: test_basic type: function
# node name: prompt type: method
# node name: _print_llm_event type: method
# -------------------

# ========================

# INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
# === Calling Function ===
# Calling function: return_info with args: {
# "node_name": "prompt",
# "class_name": "LLMPredictor"
# }
# Got output: The following is the code related to the node requested in the network graph found in the file represented by the path:
# Path: /llama_index/llm_predictor/base.py
# -------------------

# -------------------

# ========================

# INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
# === Calling Function ===
# Calling function: return_info with args: {
# "node_name": "_print_llm_event",
# "class_name": "LLMPredictor"
# }
# Got output: The following is the code related to the node requested in the network graph found in the file represented by the path:
# Path: /llama_index/llm_predictor/base.py
# -------------------