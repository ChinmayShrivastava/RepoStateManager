class ChatMode(str, Enum):
    """Chat Engine Modes."""

    SIMPLE = "simple"
    """Corresponds to `SimpleChatEngine`.

    Chat with LLM, without making use of a knowledge base.
    """

    CONDENSE_QUESTION = "condense_question"
    """Corresponds to `CondenseQuestionChatEngine`.

    First generate a standalone question from conversation context and last message,
    then query the query engine for a response.
    """

    CONTEXT = "context"
    """Corresponds to `ContextChatEngine`.

    First retrieve text from the index using the user's message, then use the context
    in the system prompt to generate a response.
    """

    CONDENSE_PLUS_CONTEXT = "condense_plus_context"
    """Corresponds to `CondensePlusContextChatEngine`.

    First condense a conversation and latest user message to a standalone question.
    Then build a context for the standalone question from a retriever,
    Then pass the context along with prompt and user message to LLM to generate a response.
    """

    REACT = "react"
    """Corresponds to `ReActAgent`.

    Use a ReAct agent loop with query engine tools.
    """

    OPENAI = "openai"
    """Corresponds to `OpenAIAgent`.

    Use an OpenAI function calling agent loop.

    NOTE: only works with OpenAI models that support function calling API.
    """

    BEST = "best"
    """Select the best chat engine based on the current LLM.

    Corresponds to `OpenAIAgent` if using an OpenAI model that supports
    function calling API, otherwise, corresponds to `ReActAgent`.
    """
