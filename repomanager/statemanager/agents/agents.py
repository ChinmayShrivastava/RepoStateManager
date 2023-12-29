from langchain.chat_models import ChatOpenAI
from langchain.tools.render import format_tool_to_openai_function
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.agents import AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage
from tools import tools

def get_langchain_llm(model="gpt-4", temperature=0):
    return ChatOpenAI(model=model, temperature=temperature)

def add_tools(llm, tools):
    llm_with_tools = llm.bind(functions=[format_tool_to_openai_function(t) for t in tools])
    return llm_with_tools

def get_prompt_template(description):
    MEMORY_KEY = "chat_history"
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are very powerful assistant, but bad at calculating lengths of words.",
            ),
            MessagesPlaceholder(variable_name=MEMORY_KEY),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

def get_agent(llm_with_tools, prompt_template):
    return (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_function_messages(
                x["intermediate_steps"]
            ),
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt_template
        | llm_with_tools
        | OpenAIFunctionsAgentOutputParser()
    )

def get_agent_executor(agent, tools, verbose=True):
    return AgentExecutor(agent=agent, tools=tools, verbose=verbose)

def chat_history(chat=None, usermessage=None, airesponse=None):
    if chat is None:
        return []
    if usermessage is not None and chat is not None:
        chat.extend([HumanMessage(content=usermessage)])
    if airesponse is not None and chat is not None:
        chat.extend([AIMessage(content=airesponse)])
    return chat

class LangchainAgent():

    def __init__(self, description, verbose=True) -> None:
        self.llm = get_langchain_llm(model='gpt-3.5-turbo-instruct')
        self.tools = []
        self.llm_with_tools = add_tools(self.llm, self.tools)
        self.prompt_template = get_prompt_template(description)
        self.agent = get_agent(self.llm_with_tools, self.prompt_template)
        self.agent_executor = get_agent_executor(self.agent, self.tools, verbose=verbose)
        self.chat = []

    def _invoke(self, input):
        # assert that the tool should not be empty
        assert len(self.tools) > 0
        result = self.agent_executor.invoke({"input": input, "chat_history": self.chat})
        self.chat = chat_history(self.chat, input, result["output"])
        return result["output"]
    
    def add_tools(self, tools):
        self.tools.extend(tools)
        self.llm_with_tools = add_tools(self.llm, self.tools)
        self.agent = get_agent(self.llm_with_tools, self.prompt_template)
        self.agent_executor = get_agent_executor(self.agent, self.tools, verbose=True)

    def set_prompt_template(self, description):
        self.prompt_template = get_prompt_template(description)
        self.agent = get_agent(self.llm_with_tools, self.prompt_template)
        self.agent_executor = get_agent_executor(self.agent, self.tools, verbose=True)

if __name__ == "__main__":
    agent = LangchainAgent("You are a database engineer, and manage a network graph of a code base repository. Help the user understand the code better by answering their queries better.")
    agent.add_tools(tools)
    # agent._invoke("What is the function get embeddings about?")
    while True:
        query = input("Enter query: ")
        agent._invoke(query)