import numpy as np
import pandas as pd
import statsmodels.api as sm
from zipline.api import attach_pipeline, pipeline_output
from zipline.pipeline import Pipeline
from zipline.pipeline.data import USEquityPricing
from zipline.pipeline.factors import AverageDollarVolume


def trend_follow_run():

    def initialize(context):
        context.lookback = 252        # Period to calculate slope and drawdown
        context.max_leverage = 1.0    # Leverage
        context.profit_take = 1.96    # 95% of bollinger band
        context.minimum_return = 0.1  # Enter if and only if annualized slope exceeds this level
        context.max_drawdown = 0.10   # Avoid if too much drawdown
        context.market_impact = 0.2   # Max order is 10% of market trading volume

        context.weights = {}          # Slope at time of entry
        context.drawdown = {}         # Drawdown at time of entry
        context.shares = {}           # Daily target share
