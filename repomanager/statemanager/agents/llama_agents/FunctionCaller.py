from llama_index.agent import OpenAIAgent
from tools import tools
from llama_index.llms.openai import OpenAI
from llama_index.llms.llm import LLM
from llama_index.memory.chat_memory_buffer import ChatMemoryBuffer
from llama_index.memory.types import BaseMemory
from llama_index.objects.base import ObjectRetriever
from llama_index.tools import BaseTool
from llama_index.callbacks import CallbackManager
from llama_index.llms.base import ChatMessage
from typing import Any, List, Optional, Type

AGENT_DESCRIPTION = (
    "As a function caller, you have access to functions that can help access a code library named 'llama index'."
    "For the user query, call the functions for the relevant information, and answer the query."
    "Collect sufficient information before answering the query."
    "If one tool doesn't give you the information you need, try another tool."
    "Always make sure that you have the right information before answering the query."
)

class FunctionManager(OpenAIAgent):

    functions_called = []
    chat_history = [ChatMessage(role="system", content=AGENT_DESCRIPTION)]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tools = tools

    # make the from tools class method inherit grom the OpenAIAgent class and add one more argument to it
    # @classmethod
    # def from_tools(
    #     cls,
    #     tools: List[BaseTool],
    #     # chat_history: List[ChatMessage],
    #     description: str = AGENT_DESCRIPTION,
    #     **kwargs: Any,
    # ) -> "FunctionManager":
    #     """Create an agent from a list of tools."""
    #     # add the tools to the kwargs
    #     chat_history = [ChatMessage(role="system", content=description)]
    #     # create the agent
    #     agent = super().from_tools(
    #         tools=tools,
    #         chat_history=chat_history,
    #         **kwargs,
    #     )
    #     return agent

    def get_function_name(self, step_result):
        """Returns the function name that was called after running a step"""
        if step_result is not None:
            return (
                step_result.output.sources[-1].content,
                step_result.output.sources[-1].tool_name, 
                step_result.output.sources[-1].raw_input,
                step_result.output.sources[-1].raw_output,
                )
        else:
            return None
        
    def run_step_and_get_function_name(self):
        """Runs a step and returns the function name that was called"""
        tid = self.get_tid_from_chat()
        step_result = self.run_step(tid)
        # add function name to list of functions called
        self.functions_called.append(self.get_function_name(step_result))
        return self.functions_called
    
    def get_tid_from_chat(self):
        """Returns the tid from a chat"""
        return list(self.state.task_dict.keys())[0]
    
    # def chat(self, message: str) -> str:
    #     chat_history = self.chat_history
    #     chat_history.append(ChatMessage(role="user", content=message))
    #     tools = self.tools

    #     ai_message = self.llm.chat(chat_history, tools=tools).message
    #     additional_kwargs = ai_message.additional_kwargs
    #     chat_history.append(ai_message)

    #     tool_calls = ai_message.additional_kwargs.get("tool_calls", None)
    #     # parallel function calling is now supported
    #     if tool_calls is not None:
    #         for tool_call in tool_calls:
    #             function_message = self._call_function(tool_call)
    #             chat_history.append(function_message)
    #             ai_message = self._llm.chat(chat_history).message
    #             chat_history.append(ai_message)

    #     return ai_message.content

    # def _call_function(self, tool_call: dict) -> ChatMessage:
    #     id_ = tool_call["id"]
    #     function_call = tool_call["function"]
    #     tool = self._tools[function_call["name"]]
    #     output = tool(**json.loads(function_call["arguments"]))
    #     return ChatMessage(
    #         name=function_call["name"],
    #         content=str(output),
    #         role="tool",
    #         additional_kwargs={
    #             "tool_call_id": id_,
    #             "name": function_call["name"],
    #         },
    #     )