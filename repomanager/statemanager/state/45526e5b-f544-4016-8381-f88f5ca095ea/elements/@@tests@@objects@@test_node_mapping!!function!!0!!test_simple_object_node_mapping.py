def test_simple_object_node_mapping() -> None:
    """Test simple object node mapping."""
    strs = ["a", "b", "c"]
    node_mapping = SimpleObjectNodeMapping.from_objects(strs)
    assert node_mapping.to_node("a").text == "a"
    assert node_mapping.from_node(node_mapping.to_node("a")) == "a"

    objects = [TestObject(name="a"), TestObject(name="b"), TestObject(name="c")]
    node_mapping = SimpleObjectNodeMapping.from_objects(objects)
    assert node_mapping.to_node(objects[0]).text == "TestObject(name='a')"
    assert node_mapping.from_node(node_mapping.to_node(objects[0])) == objects[0]
