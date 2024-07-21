def check_log_level(act_log_level: str):
    correct_levels = ['INFO', 'ERROR', 'DEBUG', 'WARN']
    act_log_level = act_log_level.upper()

    if act_log_level not in correct_levels:
        raise ValueError(
            f"{act_log_level} is not a valid value for the API_LOG_LEVEL, please try use INFO, ERROR, DEBUG or WARN"
        )

    return act_log_level
