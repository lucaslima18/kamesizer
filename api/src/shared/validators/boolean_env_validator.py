def boolean_env_validator(bool_str: str) -> bool:
    if not bool_str:
        return False

    return bool_str.lower() == 'true'
