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


def template_algorithm(src_code, capital_base, start_date, end_date, log_channel):
    logger = Logger(log_channel)

    def log(msg):
        logger.log(msg)

    local_state = {'log': log}

    byte_code = compile_restricted_exec(src_code)
    exec(byte_code.code, GLOBAL_FIELDS, local_state)  # local state may be modified

    start = pd.to_datetime(start_date).tz_localize('US/Eastern')
    end = pd.to_datetime(end_date).tz_localize('US/Eastern')

    result = run_algorithm(start, end,
                           initialize=local_state.get('initialize'),
                           handle_data=local_state.get('handle_data'),
                           before_trading_start=local_state.get('before_trading_start'),
                           capital_base=capital_base,
                           bundle='quandl')

    result.dropna(inplace=True)
    logger.close()

    return create_json_response(result)
