def prepare_subjs_param(
    subjs: Optional[List[str]], vid_type: str = "FIXED_STRING(256)"
) -> Dict:
    """Prepare parameters for query."""
    if subjs is None:
        return {}
    from nebula3.common import ttypes

    subjs_list = []
    subjs_byte = ttypes.Value()

    # filter non-digit string for INT64 vid type
    if vid_type == "INT64":
        subjs = [subj for subj in subjs if subj.isdigit()]
        if len(subjs) == 0:
            logger.warning(
                f"KG is with INT64 vid type, but no digit string is provided."
                f"Return empty subjs, and no query will be executed."
                f"subjs: {subjs}"
            )
            return {}
    for subj in subjs:
        if not isinstance(subj, str):
            raise TypeError(f"Subject should be str, but got {type(subj).__name__}.")
        subj_byte = ttypes.Value()
        if vid_type == "INT64":
            assert subj.isdigit(), (
                "Subject should be a digit string in current "
                "graph store, where vid type is INT64."
            )
            subj_byte.set_iVal(int(subj))
        else:
            subj_byte.set_sVal(subj)
        subjs_list.append(subj_byte)
    subjs_nlist = ttypes.NList(values=subjs_list)
    subjs_byte.set_lVal(subjs_nlist)
    return {"subjs": subjs_byte}
