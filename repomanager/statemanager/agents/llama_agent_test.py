from llama_agents.FunctionCaller import FunctionManager, AGENT_DESCRIPTION
from llama_agents.tools import tools as _tools
from llama_agents.tools import return_info
from llama_index.llms.openai import OpenAI
from llama_index.types import ChatMessage

if __name__ == "__main__":
    func_agent = FunctionManager.from_tools(
        tools=_tools,
        verbose=True,
        max_function_calls=5,
        llm=OpenAI('gpt-4'),
    )
    last_tuple = None
    r = func_agent.chat("""Get me the difference between agent runner and agent worker""",
    chat_history=func_agent.chat_history)
    print(r)
    while True:
        _input = input("Enter a query: ")
        r = func_agent.chat(_input)
        print(r)