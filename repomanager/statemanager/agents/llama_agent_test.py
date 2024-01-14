import sys
import os
# navigate to the parent directory, and make it as the current working directory
os.chdir("../")
sys.path.append("./")
print(os.getcwd())
print(sys.path)
from agents.llama_agents.FunctionCaller import GodFather, AGENT_INSTRUCTIONS, get_context, DEFAULT_MODEL_NAME
from vspace.pipelines.docsearch import LLMReranker
from llama_index.llms.openai import OpenAI
from llama_index.types import ChatMessage
import threading
import time
import queue

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

    func_agent = GodFather.from_tools(
        tools=[],
        verbose=False,
        # max_function_calls=5,
        llm=OpenAI('gpt-4'),
    )
    
    chat_history = [ChatMessage(role="system", content=AGENT_INSTRUCTIONS)]

    # while True:

    _input = """What are the methods available to the openaiagent class?"""
    # _input = """What are openai agents and how to initialize it from tools?"""

    # r = func_agent.chat(_input, chat_history=chat_history)

    r = func_agent.break_query(_input)

    q = queue.Queue()

    # print in green, "godfather deploys killers"
    print("\033[92m{}\033[00m".format("Godfather deploys killers!"))

    def killers(i):
        result = get_context(i)
        q.put(result)

    threads = []
    for i in range(len(r)):
        t = threading.Thread(target=killers, args=(r[i],))
        threads.append(t)
        t.start()
        time.sleep(0.1)
    for t in threads:
        t.join()

    tr = []
    while not q.empty():
        tr.extend(q.get())

    reranker = LLMReranker(OpenAI(DEFAULT_MODEL_NAME))
    reranked = reranker.rerank(_input, tr)

    # relevant information
    # rel_info = set()
    # max_len = 3
    # i = 0
    # # print tr in blue
    # print("\033[94m{}\033[00m".format(tr))
    # while True:
    #     _temp = []
    #     for j in range(len(tr)):
    #         if i < len(tr[j]):
    #             try:
    #                 _temp.append(tr[j][i])
    #             except:
    #                 pass
    #     for t in _temp:
    #         if len(rel_info) < max_len:
    #             rel_info.add(t)
    #     if len(rel_info) == max_len:
    #         break
    #     i += 1
    # rel_info = list(rel_info)

    _context = "The following is relevant information to help answer the query:\n"
    for i in range(len(reranked)):
        _context += "----------\n"
        _context += reranked[i] + "\n"

    _prompt = _context + "\nQuery: " + _input + "\nAnswer:"

    # print the prompt in red
    print("\033[91m{}\033[00m".format(_prompt))

    chat_history.append(ChatMessage(role="user", content=_prompt))
    rn = func_agent.chat(_input, chat_history=chat_history)
    print(rn)