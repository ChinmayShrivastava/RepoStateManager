class ToolType(str, enum.Enum):
    """
    An enumeration.
    """

    ALGOLIA = "ALGOLIA"
    BROWSER = "BROWSER"
    BING_SEARCH = "BING_SEARCH"
    REPLICATE = "REPLICATE"
    WOLFRAM_ALPHA = "WOLFRAM_ALPHA"
    ZAPIER_NLA = "ZAPIER_NLA"
    AGENT = "AGENT"
    OPENAPI = "OPENAPI"
    CHATGPT_PLUGIN = "CHATGPT_PLUGIN"
    METAPHOR = "METAPHOR"
    PUBMED = "PUBMED"
    CODE_EXECUTOR = "CODE_EXECUTOR"
    OPENBB = "OPENBB"
    GPT_VISION = "GPT_VISION"
    TTS_1 = "TTS_1"
    HAND_OFF = "HAND_OFF"
    FUNCTION = "FUNCTION"

    def visit(
        self,
        algolia: typing.Callable[[], T_Result],
        browser: typing.Callable[[], T_Result],
        bing_search: typing.Callable[[], T_Result],
        replicate: typing.Callable[[], T_Result],
        wolfram_alpha: typing.Callable[[], T_Result],
        zapier_nla: typing.Callable[[], T_Result],
        agent: typing.Callable[[], T_Result],
        openapi: typing.Callable[[], T_Result],
        chatgpt_plugin: typing.Callable[[], T_Result],
        metaphor: typing.Callable[[], T_Result],
        pubmed: typing.Callable[[], T_Result],
        code_executor: typing.Callable[[], T_Result],
        openbb: typing.Callable[[], T_Result],
        gpt_vision: typing.Callable[[], T_Result],
        tts_1: typing.Callable[[], T_Result],
        hand_off: typing.Callable[[], T_Result],
        function: typing.Callable[[], T_Result],
    ) -> T_Result:
        if self is ToolType.ALGOLIA:
            return algolia()
        if self is ToolType.BROWSER:
            return browser()
        if self is ToolType.BING_SEARCH:
            return bing_search()
        if self is ToolType.REPLICATE:
            return replicate()
        if self is ToolType.WOLFRAM_ALPHA:
            return wolfram_alpha()
        if self is ToolType.ZAPIER_NLA:
            return zapier_nla()
        if self is ToolType.AGENT:
            return agent()
        if self is ToolType.OPENAPI:
            return openapi()
        if self is ToolType.CHATGPT_PLUGIN:
            return chatgpt_plugin()
        if self is ToolType.METAPHOR:
            return metaphor()
        if self is ToolType.PUBMED:
            return pubmed()
        if self is ToolType.CODE_EXECUTOR:
            return code_executor()
        if self is ToolType.OPENBB:
            return openbb()
        if self is ToolType.GPT_VISION:
            return gpt_vision()
        if self is ToolType.TTS_1:
            return tts_1()
        if self is ToolType.HAND_OFF:
            return hand_off()
        if self is ToolType.FUNCTION:
            return function()
