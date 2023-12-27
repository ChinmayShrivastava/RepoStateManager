def _substack_reader(soup: Any) -> Tuple[str, Dict[str, Any]]:
    """Extract text from Substack blog post."""
    metadata = {
        "Title of this Substack post": soup.select_one("h1.post-title").getText(),
        "Subtitle": soup.select_one("h3.subtitle").getText(),
        "Author": soup.select_one("span.byline-names").getText(),
    }
    text = soup.select_one("div.available-content").getText()
    return text, metadata
