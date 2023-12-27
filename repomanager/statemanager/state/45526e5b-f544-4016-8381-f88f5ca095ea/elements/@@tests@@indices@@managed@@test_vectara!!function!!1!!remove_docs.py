def remove_docs(index: VectaraIndex, ids: List) -> None:
    for id in ids:
        index._delete_doc(id)
