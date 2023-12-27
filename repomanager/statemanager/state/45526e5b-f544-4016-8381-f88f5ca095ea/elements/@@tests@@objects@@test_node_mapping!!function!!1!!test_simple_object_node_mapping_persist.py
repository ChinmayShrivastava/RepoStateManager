def test_simple_object_node_mapping_persist() -> None:
    """Test persist/load."""
    strs = ["a", "b", "c"]
    node_mapping = SimpleObjectNodeMapping.from_objects(strs)
    node_mapping.persist()

    loaded_node_mapping = SimpleObjectNodeMapping.from_persist_dir()
    assert node_mapping.obj_node_mapping == loaded_node_mapping.obj_node_mapping
