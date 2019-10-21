from RestrictedPython import compile_restricted_exec

# Zipline API
from zipline import run_algorithm

# Dataframe
import pandas as pd

# Data frame to JSON
from .allowed_imports import GLOBAL_FIELDS

# Logging
from backend.api.logger import Logger

from backend.api.create_response import create_json_response
from .filter_error_msg import filter_error_msg


def template_algorithm(src_code, capital_base, start_date, end_date, log_channel):
    logger = Logger(log_channel)

    def log(msg):
        logger.log(msg)

    local_fields = {'log': log}
    local_state = {}

    byte_code = compile_restricted_exec(src_code)

    if len(byte_code.errors) != 0:
        log('COMPILE ERROR =====')
        for error in byte_code.errors:
            formatted_error = error.replace('"', "'")
            log(formatted_error)
        logger.close()
        return {
            'done': True,
            'success': False,
        }

    exec(byte_code.code, {**GLOBAL_FIELDS, **local_fields}, local_state)  # local state may be modified

    start = pd.to_datetime(start_date).tz_localize('US/Eastern')
    end = pd.to_datetime(end_date).tz_localize('US/Eastern')

    try:
        result = run_algorithm(start, end,
                               initialize=local_state.get('initialize'),
                               handle_data=local_state.get('handle_data'),
                               before_trading_start=local_state.get('before_trading_start'),
                               capital_base=capital_base,
                               bundle='quandl')

        result.dropna(inplace=True)
        logger.close()
        return create_json_response(result)
    except Exception as e:
        error_msg = str(e)
        log('RUNTIME ERROR ====')

        if not filter_error_msg(error_msg):
            log(error_msg)

        return {
            'done': True,
            'success': False,
        }
