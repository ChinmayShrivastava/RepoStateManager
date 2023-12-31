from llama_agents.FunctionCaller import FunctionManager, AGENT_DESCRIPTION
from llama_agents.tools import tools as _tools
from llama_agents.tools import return_info
from llama_index.llms.openai import OpenAI
from llama_index.types import ChatMessage
# from llama_index.vector_stores import V

if __name__ == "__main__":
    func_agent = FunctionManager.from_tools(
        tools=_tools,
        verbose=True,
        max_function_calls=5,
        llm=OpenAI('gpt-4'),
    )
    last_tuple = None
    # while True:
    r = func_agent.chat("""Hello everyone! I have a question about the OpenAIPromptExecutionSettings ToolCallBehaviour.AutoInvokeKernelFunctions.

I understand how to use it, and witness that it can create automatically a plan on its own to generate in a certain order the functions that are inside the plugins registered into the Kernel. However I don't understand how it works under the hood. Does it use SK planner ? Is this embedded inside OpenAI ChatGPT ?""",
                        chat_history=func_agent.chat_history)
    print(r)