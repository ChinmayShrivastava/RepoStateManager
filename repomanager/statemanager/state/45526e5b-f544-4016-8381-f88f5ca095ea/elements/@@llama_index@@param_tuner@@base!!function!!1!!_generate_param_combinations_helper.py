    def _generate_param_combinations_helper(
        param_dict: Dict[str, Any], curr_param_dict: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Helper function."""
        if len(param_dict) == 0:
            return [deepcopy(curr_param_dict)]
        param_dict = deepcopy(param_dict)
        param_name, param_vals = param_dict.popitem()
        param_combinations = []
        for param_val in param_vals:
            curr_param_dict[param_name] = param_val
            param_combinations.extend(
                _generate_param_combinations_helper(param_dict, curr_param_dict)
            )
        return param_combinations
