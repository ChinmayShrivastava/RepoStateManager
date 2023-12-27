def tokenize_remove_stopwords(text: str) -> List[str]:
    stemmer = PorterStemmer()
    words = list(simple_extract_keywords(text))
    return [stemmer.stem(word) for word in words]
