import numpy as np
import pandas as pd
import statsmodels.api as sm
from zipline.api import attach_pipeline, pipeline_output
from zipline.pipeline import Pipeline
from zipline.pipeline.data import USEquityPricing
from zipline.pipeline.factors import AverageDollarVolume