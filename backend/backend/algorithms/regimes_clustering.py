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

# Logging
from websocket import create_connection

# Data frame to JSON
from ..api.create_response import create_json_response


def regimes_clustering_run(start_date, end_date, capital_base, ticker, use_clf, no_shorts, log_channel):

    ws = create_connection("ws://alpharithmic.herokuapp.com/ws/logs/%s/" % log_channel)
    msg_placeholder = "{\"message\": \"%s\"}"

    ws.send(msg_placeholder % "Link Start")

    def initialize(context):

        ws.send(msg_placeholder % "Simulation Start")

        context.security = symbol(ticker)
        context.long_threshold = 0
        context.short_threshold = -0.06

        context.no_shorts = no_shorts

        if context.no_shorts:
            set_long_only()

        context.n_clusters = 9
        context.ret_windows = [30]
        context.window_lengths = [30, 90, 150, 210, 240]
        context.lookback = 8 * 250
        context.refresh_frequency = 30

        context.use_classifier = use_clf

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

        ws.send(msg_placeholder % "Execution of clustering scheduled at 1 hour after market open")

    def before_trading_start(context, data):
        context.days_traded += 1

        if context.model == {} or context.model['refresh_date'] <= context.days_traded:
            context.model['refresh_date'] = context.days_traded + context.refresh_frequency
            clusters = {}

            ws.send(msg_placeholder % "Retraining the clustering ML model")

            for ret_window in context.ret_windows:
                clusters[ret_window] = {'windows': {}}

                for window_length in context.window_lengths:
                    cluster_data = create_kmeans_features(context, data, window_length, ret_window)

                    window_length_str = str(window_length)

                    ws.send(msg_placeholder % ("Feature set for k-means with a look back of %s days created"
                                               % window_length_str))

                    cluster_data.dropna(inplace=True)
                    X = cluster_data.drop('rets', axis=1)
                    y = cluster_data['rets']

                    kmeans = KMeans(n_clusters=context.n_clusters, n_init=100, max_iter=500, random_state=42,
                                    precompute_distances=True)
                    kmeans.fit(X)

                    ws.send(msg_placeholder % ("K-means cluster for look back of %s days trained" % window_length_str))

                    clusters[ret_window]['windows'][window_length] = {
                        "kmeans": kmeans,
                        "regimes": kmeans.predict(X),
                        "rets": y
                    }

            ws.send(msg_placeholder % "Retraining the Random Forest ML model")

            panel = create_rand_forest_features(clusters)

            ws.send(msg_placeholder % "Feature set for Random Forest created")

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

                    ws.send(msg_placeholder % "Random Forest Classifier trained")

                else:
                    rfr = RandomForestRegressor(n_estimators=1000, random_state=42)
                    rfr.fit(X_train, ret.values)
                    clusters[ret_window]['reg'] = rfr

                    ws.send(msg_placeholder % "Random Forest Regression trained")

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

                window_length_str = str(window_length)

                ws.send(msg_placeholder % ("Adjusting clusters for the K-means with a look back of %s days"
                                           % window_length_str))

                cluster_data = create_kmeans_features(context, data, window_length, ret_window, for_training=False)
                X = cluster_data.drop('rets', axis=1)
                y = cluster_data['rets']

                ws.send(msg_placeholder % ("New feature set created for the K-means with a look back of %s days"
                                           % window_length_str))

                kmeans = clusters[ret_window]['windows'][window_length]['kmeans']
                clusters[ret_window]['windows'][window_length]['regimes'] = kmeans.predict(X.values)
                clusters[ret_window]['windows'][window_length]['rets'] = y  # set all y's to NaN

                ws.send(msg_placeholder % ("New clusters generated for the K-means with a look back of %s days"
                                           % window_length_str))

        panel = create_rand_forest_features(clusters)

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

                    vectorized_ret_buckets = np.array(ret_buckets)

                    v = [ret_buckets[0] - 1] \
                        + list(0.5 * (vectorized_ret_buckets[1:] + vectorized_ret_buckets[:-1])) \
                        + [ret_buckets[-1] + 1]

                    v = np.array(v)

                    est = v[prediction]

            else:
                reg = classifier['reg']
                est = reg.predict(X.values)

            context.return_projections[ret_window] = est
            projection_date = context.days_traded + ret_window
            context.price_projections[projection_date] = (1 + est) * data.current(context.security, 'price')

            ws.send(msg_placeholder % ("Random Forest produced a projected return of %s and price change of %s"
                    % (str(est), str(context.price_projections[projection_date]))))

        execute_transactions(context)

    def execute_transactions(context):
        if len(context.ret_windows) == 1:
            key = context.ret_windows[0]

            if context.use_classifier:
                probs = context.bucket_probs[key]
                p = sum(probs[2:])

                if p > context.long_prob_lb:
                    order_target_percent(context.security, 1)
                    context.last_traded_date = context.days_traded

                    ws.send(msg_placeholder % ("Bought %s because probability %s is greater than lower bound %s"
                                               % (str(context.security), str(p), str(context.long_prob_lb))))

                elif p < context.short_prob_ub:
                    order_target_percent(context.security, context.no_shorts - 1)
                    context.last_traded_date = context.days_traded

                    ws.send(msg_placeholder % ("Shorted %s because probability %s is lower than upper bound %s"
                                               % (str(context.security), str(p), str(context.short_prob_ub))))

                else:
                    order_target_percent(context.security, 0)

                    ws.send(msg_placeholder % ("Sold %s" % str(context.security)))

            else:
                estimate = context.return_projections[key]

                if estimate > context.long_threshold:
                    order_target_percent(context.security, 1)
                    context.last_traded_date = context.days_traded

                    ws.send(msg_placeholder % ("Bought %s because estimate %s is greater than threshold %s"
                                               % (str(context.security), str(estimate), str(context.long_threshold))))

                elif estimate < context.short_threshold:
                    order_target_percent(context.security, context.no_shorts - 1)
                    context.last_traded_date = context.days_traded

                    ws.send(msg_placeholder % ("Shorted %s because estimate %s is lower than threshold %s"
                                               % (str(context.security), str(estimate), str(context.short_threshold))))

                else:
                    order_target_percent(context.security, 0)

                    ws.send(msg_placeholder % ("Sold %s" % str(context.security)))

    def create_kmeans_features(context, data, window_length, ret_window, for_training=True):
        lookback = context.lookback if for_training else window_length + 1
        ts = data.history(context.security, ['price', 'volume'], lookback, '1d')
        ts.dropna(inplace=True)
        ts['ret'] = ts['price'] / ts['price'].shift(1) - 1

        volatility = {}
        resids = {}
        trends = {}

        rets_deque = deque(maxlen=window_length)
        prices_deque = deque(maxlen=window_length)

        length = len(ts)

        for i in range(1, length):
            rets_deque.append(ts['ret'].iloc[i])
            prices_deque.append(ts['price'].iloc[i])

            if len(rets_deque) == rets_deque.maxlen:

                regression_result = sm.OLS(np.array(prices_deque) / prices_deque[0],
                                           sm.add_constant(range(prices_deque.maxlen)),
                                           hasconst=True)\
                                    .fit()

                volatility[ts.index[i]] = np.std(rets_deque, ddof=1) * np.sqrt(252)
                resids[ts.index[i]] = regression_result.resid.std(ddof=1)

                global beta

                if regression_result.pvalues[1] < 0.05:
                    beta = regression_result.params[1]
                else:
                    beta = 0

                trends[ts.index[i]] = beta * 100

        sigs = pd.Series(volatility, name='sig')
        betas = pd.Series(trends, name='beta')
        residuals = pd.Series(resids, name='resid')

        global y_rets

        if for_training:
            y_rets = ts['price'] / ts['price'].shift(ret_window) - 1
            y_rets.name = "rets"

            df = pd.DataFrame([sigs, betas, residuals, y_rets]).T

            return df

        else:
            df = pd.DataFrame([sigs, betas, residuals]).T

            df['rets'] = np.nan

            return df

    def create_rand_forest_features(clusters):

        ret_windows = clusters.keys()

        def extract(ret_window_param):
            min_regime_len = min([len(d['regimes']) for wl, d in clusters[ret_window_param]['windows'].items()])

            collector = {}

            for wl, d in clusters[ret_window_param]['windows'].items():
                try:
                    collector[wl] = d['regimes'][-min_regime_len:]
                except TypeError:
                    pass

            df = pd.DataFrame(collector)

            ret = d['rets'].values[-min_regime_len:]
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

    ws.send(msg_placeholder % "Simulation End")
    ws.send(msg_placeholder % "Fetching backtest results from Redis Queue...")

    result.dropna(inplace=True)
    ws.close()

    return create_json_response(result)
