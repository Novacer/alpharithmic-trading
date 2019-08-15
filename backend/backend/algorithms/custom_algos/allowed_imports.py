# Zipline API
from zipline.pipeline import Pipeline
from zipline.api import attach_pipeline, pipeline_output, schedule_function, order, order_target_percent, symbol
from zipline.pipeline.factors import AverageDollarVolume
from zipline.utils.events import date_rules, time_rules

# Data frame
import numpy as np
import pandas as pd
from scipy import stats

ALLOWED_IMPORTS = {
    'Pipeline': Pipeline,
    'attach_pipeline': attach_pipeline,
    'pipeline_output': pipeline_output,
    'schedule_function': schedule_function,
    'order': order,
    'order_target_percent': order_target_percent,
    'symbol': symbol,
    'AverageDollarVolume': AverageDollarVolume,
    'date_rules': date_rules,
    'time_rules': time_rules,
    'np': np,
    'pd': pd,
    'stats': stats,
}

GLOBAL_FIELDS = {
    '__builtins__': {
        'str': str,
        'len': len,
    },
    '__metaclass__': type,
    '_write_': lambda x: x,
    '_getattr_': getattr,
    '_setattr_': setattr,
    **ALLOWED_IMPORTS
}
