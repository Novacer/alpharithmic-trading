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

    def get_cluster_data(context, data, window_length, ret_window, for_training=True):
        L = context.lookback if for_training else window_length + 1
        ts = data.history(context.security_list, ['price', 'volume'], L, '1d')
        ts.dropna(inplace=True)
        ts['ret'] = ts['price'] / ts['price'].shift(1) - 1

        vols = {}
        volumes = {}
        resids = {}
        trends = {}

        volume_deque = deque(maxlen=window_length)
        rets_deque = deque(maxlen=window_length)
        prices_deque = deque(maxlen=window_length)

        length = len(ts)

        for i in range(1, length):
            rets_deque.append(ts['ret'].iloc[i])
            prices_deque.append(ts['price'].iloc[i])
            volume_deque.append(ts['volume'].iloc[i])

            if len(rets_deque) == rets_deque.maxlen:
                volumes[ts.index[i]] = sum(volume_deque) / 1e9

                regression_result = sm.OLS(np.array(prices_deque) / prices_deque[0],
                                           sm.add_constant(range(prices_deque.maxlen)),
                                           hasconst=True)\
                                    .fit()

                vols[ts.index[i]] = np.std(rets_deque, ddof=1) * np.sqrt(252)
                resids[ts.index[i]] = regression_result.resid.std(ddof=1)

                global beta

                if regression_result.pvalues[1] < 0.05:
                    beta = regression_result.params[1]
                else:
                    beta = 0

                trends[ts.index[i]] = beta

        sigs = pd.Series(vols, name='sig')
        betas = pd.Series(trends, name='beta')
        resids = pd.Series(resids, name='resid')
        volumes = pd.Series(volumes, name='volume')

        global y_rets

        if for_training:
            y_rets = ts['price'] / ts['price'].shift(ret_window) - 1
            y_rets.name = "rets"

        else:
            y_rets = sigs.copy() * np.nan
            y_rets.name = "rets"

        df = pd.DataFrame([sigs, betas, resids, volumes]).T
        df.drop('volume', axis=1)

        df['beta'] *= 100

        return df

    def get_X(clusters):

        ret_windows = clusters.keys()

        def extract(ret_window):
            l = min([len(d['regimes']) for wl, d in clusters[ret_window]['windows'].items()])

            collector = {}

            for wl, d in clusters[ret_window]['windows'].items():
                try:
                    collector[wl] = d['regimes'][-l:]
                except TypeError:
                    pass

            df = pd.DataFrame(collector)

            ret = d['rets'].values[-l:]
            df['rets'] = ret

            return df

        output = {}

        for ret_window in ret_windows:
            output[ret_window] = extract(ret_window)

        return pd.Panel(output)