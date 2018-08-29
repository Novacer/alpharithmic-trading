# Zipline API
from zipline.api import symbol, set_long_only, order_target_percent, schedule_function
from zipline.utils.events import date_rules, time_rules
from zipline import run_algorithm

# Data frame
import numpy as np
import pandas as pd
import statsmodels.api as sm

# Machine Learning
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.multiclass import OneVsRestClassifier

# Data structures
from collections import deque


def regimes_clustering_run(start_date, end_date, capital_base, log_channel):

    def initialize(context):
        context.security = symbol("AAPL")
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
        context.last_traded_date = 0

        schedule_function(rebalance, date_rule=date_rules.every_day(), time_rule=time_rules.market_open(hours=1))


    def before_trading_start(context, data):
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

    def rebalance(context, data):
        if context.last_traded_date != 0 \
                and context.days_traded < context.last_traded_date + (context.ret_windows[0] * 7/5):

            return

        try:
            clusters = context.model['clusters']
        except KeyError:
            return

        for ret_window in context.ret_windows:
            for window_length in context.window_lengths:
                cluster_data = get_cluster_data(context, data, window_length, ret_window, for_training=False)
                X = cluster_data.drop('rets', axis=1)
                y = cluster_data['rets']

                kmeans = clusters[ret_window]['windows'][window_length]['kmeans']
                clusters[ret_window]['windows'][window_length]['regimes'] = kmeans.predict(X.values)
                clusters[ret_window]['windows'][window_length]['rets'] = y

        panel = get_X(clusters)

        for ret_window, classifier in clusters.items():
            df = panel[ret_window]
            X = df.drop('rets', axis=1)

            global est

            if context.use_classifier:

                global ret_buckets

                try:
                    ret_buckets = context.ret_buckets[ret_window]
                except KeyError:
                    ret_buckets = context.ret_buckets['gen']

                clf = classifier['clf']

                prediction = clf.predict(X.values)
                context.bucket_probs[ret_window] = clf.predict_proba(X.values)[0]

                if len(ret_buckets) == 1:
                    est = ret_buckets[0] + 2 * prediction - 1
                else:
                    v = [ret_buckets[0] - 1] \
                        + list(0.5 * (np.array(ret_buckets)[1:] + np.array(ret_buckets)[:-1])) \
                        + [ret_buckets[-1] + 1]
                    est = v[prediction]

            else:
                reg = classifier['reg']
                est = reg.predict(X.values)

            context.return_projections[ret_window] = est
            projection_date = context.days_traded + ret_window
            context.price_projections[projection_date] = (1 + est) * data.current(context.security, 'price')

        make_trade(context, data)

    def make_trade(context, data):
        if len(context.ret_windows) == 1:
            key = context.ret_windows[0]

            if context.use_classifier:
                probs = context.bucket_probs[key]
                p = sum(probs[2:])

                if p > context.long_prob_lb:
                    order_target_percent(context.security, 1)
                    context.last_traded_date = context.days_traded

                    print("bought")

                elif p < context.short_prob_ub:
                    order_target_percent(context.security, context.long_only - 1)
                    context.last_traded_date = context.days_traded

                    print("shorted")

                else:
                    order_target_percent(context.security, 0)
                    print("sold")

            else:
                estimate = context.return_projections[key]

                if estimate > context.long_threshold:
                    order_target_percent(context.security, 1)
                    context.last_traded_date = context.days_traded

                    print('bought')

                elif estimate < context.short_threshold:
                    order_target_percent(context.security, context.long_only - 1)
                    context.last_traded_date = context.days_traded

                    print('shorted')
                else:
                    order_target_percent(context.security, 0)

                    print('sold')

    def get_cluster_data(context, data, window_length, ret_window, for_training=True):
        L = context.lookback if for_training else window_length + 1
        ts = data.history(context.security, ['price', 'volume'], L, '1d')
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

        df = pd.DataFrame([sigs, betas, resids, volumes, y_rets]).T
        df.drop('volume', axis=1, inplace=True)

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

    start = pd.to_datetime(start_date).tz_localize('US/Eastern')
    end = pd.to_datetime(end_date).tz_localize('US/Eastern')

    result = run_algorithm(start, end,
                           initialize=initialize, before_trading_start=before_trading_start,
                           capital_base=capital_base,
                           bundle="quantopian-quandl")

    return result


result = regimes_clustering_run("2016-01-01", "2017-01-01", 1000000, "abc")

print(result.head())
