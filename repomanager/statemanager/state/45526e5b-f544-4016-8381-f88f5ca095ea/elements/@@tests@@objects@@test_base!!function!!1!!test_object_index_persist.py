def test_object_index_persist(mock_service_context: ServiceContext) -> None:
    """Test object index persist/load."""
    object_mapping = SimpleObjectNodeMapping.from_objects(["a", "b", "c"])
    obj_index = ObjectIndex.from_objects(
        ["a", "b", "c"], object_mapping, index_cls=SummaryIndex
    )
    obj_index.persist()

    reloaded_obj_index = ObjectIndex.from_persist_dir()
    assert obj_index._index.index_id == reloaded_obj_index._index.index_id
    assert obj_index._index.index_struct == reloaded_obj_index._index.index_struct
    assert (
        obj_index._object_node_mapping.obj_node_mapping
        == reloaded_obj_index._object_node_mapping.obj_node_mapping
    )

    # version where user passes in the object_node_mapping
    reloaded_obj_index = ObjectIndex.from_persist_dir(
        object_node_mapping=object_mapping
    )
    assert obj_index._index.index_id == reloaded_obj_index._index.index_id
    assert obj_index._index.index_struct == reloaded_obj_index._index.index_struct
    assert (
        obj_index._object_node_mapping.obj_node_mapping
        == reloaded_obj_index._object_node_mapping.obj_node_mapping
    )
