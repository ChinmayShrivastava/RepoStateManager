def test_get_biggest_prompt() -> None:
    """Test get_biggest_prompt from PromptHelper."""
    prompt1 = PromptTemplate("This is the prompt{text}")
    prompt2 = PromptTemplate("This is the longer prompt{text}")
    prompt3 = PromptTemplate("This is the {text}")
    biggest_prompt = get_biggest_prompt([prompt1, prompt2, prompt3])

    assert biggest_prompt == prompt2
