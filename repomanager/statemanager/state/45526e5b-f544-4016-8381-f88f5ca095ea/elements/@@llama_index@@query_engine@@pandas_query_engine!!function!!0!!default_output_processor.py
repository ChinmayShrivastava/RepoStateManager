def default_output_processor(
    output: str, df: pd.DataFrame, **output_kwargs: Any
) -> str:
    """Process outputs in a default manner."""
    import ast
    import sys
    import traceback

    if sys.version_info < (3, 9):
        logger.warning(
            "Python version must be >= 3.9 in order to use "
            "the default output processor, which executes "
            "the Python query. Instead, we will return the "
            "raw Python instructions as a string."
        )
        return output

    local_vars = {"df": df}

    # NOTE: inspired from langchain's tool
    # see langchain.tools.python.tool (PythonAstREPLTool)
    try:
        tree = ast.parse(output)
        module = ast.Module(tree.body[:-1], type_ignores=[])
        safe_exec(ast.unparse(module), {}, local_vars)  # type: ignore
        module_end = ast.Module(tree.body[-1:], type_ignores=[])
        module_end_str = ast.unparse(module_end)  # type: ignore
        if module_end_str.strip("'\"") != module_end_str:
            # if there's leading/trailing quotes, then we need to eval
            # string to get the actual expression
            module_end_str = safe_eval(module_end_str, {"np": np}, local_vars)
        try:
            # str(pd.dataframe) will truncate output by display.max_colwidth
            # set width temporarily to extract more text
            if "max_colwidth" in output_kwargs:
                pd.set_option("display.max_colwidth", output_kwargs["max_colwidth"])
            output_str = str(safe_eval(module_end_str, {"np": np}, local_vars))
            pd.reset_option("display.max_colwidth")
            return output_str

        except Exception:
            raise
    except Exception as e:
        err_string = (
            "There was an error running the output as Python code. "
            f"Error message: {e}"
        )
        traceback.print_exc()
        return err_string
