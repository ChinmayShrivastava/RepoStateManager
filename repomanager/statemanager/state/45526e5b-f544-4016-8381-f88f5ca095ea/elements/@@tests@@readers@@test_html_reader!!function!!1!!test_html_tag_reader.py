def test_html_tag_reader(html_str: str) -> None:
    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=".html"
    ) as temp_file:
        temp_file.write(html_str)
        temp_file_path = Path(temp_file.name)

    reader = HTMLTagReader(ignore_no_id=True)
    docs = reader.load_data(temp_file_path)
    assert len(docs) == 2
    assert docs[0].metadata["tag_id"] == "about"
    assert docs[1].metadata["tag_id"] == "services"

    reader = HTMLTagReader()
    docs = reader.load_data(temp_file_path)
    assert len(docs) == 3
    assert docs[2].metadata["tag_id"] is None

    os.remove(temp_file.name)
