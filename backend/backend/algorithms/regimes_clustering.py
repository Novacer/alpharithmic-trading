# Zipline API
from zipline.api import attach_pipeline, pipeline_output, symbol, set_long_only
from zipline.pipeline import Pipeline
from zipline.pipeline.data import USEquityPricing
from zipline.pipeline.factors import AverageDollarVolume

# Math
import numpy as np
import pandas as pd
from scipy import optimize
from scipy import stats
import statsmodels.api as sm

# Date
import datetime

# Machine Learning
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Data structures
from collections import deque


def regimes_clustering_run():

    def initialize(context):
        context.security = symbol("AAPL")
        context.long_threshold = 0
        context.short_threshold = -0.06

        context.no_shorts = False

        if context.no_shorts:
            set_long_only()

        context.n_clusters = 9
        context.ret_windows = [30]
        context.window_length = [15, 30, 60, 90, 120, 150, 180, 210, 240]
        context.lookback = 8 * 250
        context.refresh_frequency = 30

        context.use_classifier = True

        if context.use_classifier:
            context.ret_buckets = {
                "gen": [-0.04, 0, 0.04]
            }

        context.long_prob_lb = 0.5
        context.short_prob_ub = 0.3

        context.model = {}
        context.return_projections = {}
        context.price_projections = {}
        context.bucket_probs = {}

        attach_pipeline(create_high_dollar_volume_pipeline(), 'top_dollar_volume')

    def create_high_dollar_volume_pipeline():
        pipe = Pipeline()

        dollar_volume = AverageDollarVolume(window_length=63)  # 63 days = 1 quarter
        pipe.add(dollar_volume, 'dollar_volume')

        high_dollar_volume = dollar_volume.percentile_between(95, 100)  # top 5% by dollar volume
        pipe.set_screen(high_dollar_volume)

        return pipe
