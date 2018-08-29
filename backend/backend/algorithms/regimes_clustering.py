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
        context.security_list = []
        context.long_threshold = 0
        context.short_threshold = -0.06

        context.no_shorts = False

        if context.no_shorts:
            set_long_only()

        context.n_clusters = 9
        context.ret_windows = [30]
        context.window_lengths = [15, 30, 60, 90, 120, 150, 180, 210, 240]
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

        context.days_traded = 0

        attach_pipeline(create_high_dollar_volume_pipeline(), 'tdv')

    def create_high_dollar_volume_pipeline():
        pipe = Pipeline()

        dollar_volume = AverageDollarVolume(window_length=63)
        pipe.add(dollar_volume, 'dollar_volume')

        high_dollar_volume = dollar_volume.percentile_between(99, 100)  # top 1% by dollar volume
        pipe.set_screen(high_dollar_volume)

        return pipe

    def before_trading_start(context, data):
        context.output = pipeline_output('tdv')
        context.security_list = context.output.index

        context.days_traded += 1

        if context.model == {} or context.model['refresh_date'] <= context.days_traded:
            context.model['refresh_date'] = context.days_traded + context.refresh_frequency
            clusters = {}

            for ret_window in context.ret_windows:
                clusters[ret_window] = {'windows': {}}

                for window_length in context.window_lengths:
                    cluster_data = get_cluster_data(context, data, window_length, ret_window)
                    cluster_data.dropna(inplace=True)
                    X = cluster_data.drop('rets', axis=1)
                    y = cluster_data['rets']

                    kmeans = KMeans(n_clusters=context.n_clusters, n_init=100, max_iter=500, random_state=42)
                    kmeans.fit(X)
                    clusters[ret_window]['windows'][window_length] = {
                        "kmeans": kmeans,
                        "regimes": kmeans.predict(X),
                        "rets": y
                    }

            panel = get_X(clusters)

            for ret_window, _ in clusters.items():
                df = panel[ret_window]
                ret = df['rets']

                X = df.drop('rets', axis=1)
                X_train = X.values

                if context.use_classifier:

                    global ret_buckets

                    try:
                        ret_buckets = context.ret_buckets[ret_window]
                    except KeyError:
                        ret_buckets = context.ret_buckets['gen']

                    clf = OneVsRestClassifier(RandomForestClassifier(n_estimators=1000, random_state=42))

                    y = len(ret_buckets) * np.ones(len(ret)).astype(int)

                    for i in range(len(ret_buckets) - 1, -1, -1):
                        I = ret.values < ret_buckets[i]

                        y[I] = i

                    y_train = y

                    clf.fit(X_train, y_train)
                    clusters[ret_window]['clf'] = clf

                else:
                    rfr = RandomForestRegressor(n_estimators=1000, random_state=42)
                    rfr.fit(X_train, ret.values)
                    clusters[ret_window]['reg'] = rfr

            context.model['clusters'] = clusters
