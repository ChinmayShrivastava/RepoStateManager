def test_validates_api_key_is_present() -> None:
    with CachedOpenAIApiKeys():
        os.environ["OPENAI_API_KEY"] = "sk-" + ("a" * 48)

        # We can create a new LLM when the env variable is set
        assert OpenAI()

        os.environ["OPENAI_API_KEY"] = ""

        # We can create a new LLM when the api_key is set on the
        # class directly
        assert OpenAI(api_key="sk-" + ("a" * 48))
