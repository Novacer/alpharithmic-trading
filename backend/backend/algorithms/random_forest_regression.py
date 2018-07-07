from sklearn.ensemble import RandomForestRegressor
import numpy as np
import pandas as pd
from zipline.api import schedule_function, order_target_percent, symbol
from zipline.utils.events import date_rules, time_rules
from zipline import run_algorithm

import matplotlib.pyplot as plt

def rfr_run(start_date, end_date, capital_base, ticker):

    def initialize(context):
        context.security = symbol(ticker)
        context.model = RandomForestRegressor()
        context.trained = False

        context.lookback = 3
        context.history_range = 400

        schedule_function(create_model, date_rules.week_end(), time_rules.market_close(minutes=10))

        schedule_function(trade, date_rules.every_day(), time_rules.market_open(minutes=1))


    def create_model(context, data):
        recent_prices = data.history(assets=context.security, bar_count=context.history_range,
                                     frequency="1d", fields="price").values

        price_changes = np.diff(recent_prices).tolist()

        X = []
        y = []

        for i in range(context.history_range - context.lookback - 1):
            X.append(price_changes[i: i + context.lookback])  # historical price changes
            y.append(price_changes[i + context.lookback])  # today's price change

        context.model.fit(X, y)  # train the ML model

        if len(y) > 1:
            context.trained = True


    def trade(context, data):

        if context.trained and context.model:
            recent_prices = data.history(assets=context.security, bar_count=context.lookback + 1,
                                         frequency='1d', fields='price').values

            price_changes = np.diff(recent_prices).reshape(1, -1)

            prediction = context.model.predict(price_changes)

            print("Predicted Change is", prediction)

            if prediction > 0:
                order_target_percent(context.security, 1.0)
                print("Bought 100% of portfolio")
            else:
                order_target_percent(context.security, -1.0)
                print("Shorted 100% of portfolio")


    def handle_data(context, data):
        pass


    start = pd.to_datetime(start_date).tz_localize('US/Eastern')
    end = pd.to_datetime(end_date).tz_localize('US/Eastern')

    result = run_algorithm(start, end, initialize=initialize,
                           handle_data=handle_data,
                           capital_base=capital_base, bundle='quantopian-quandl')

    result.dropna(inplace=True)

    return result


result = rfr_run("2016-01-01", "2017-01-01", 1000000, "MSFT")

plt.plot(result['algorithm_period_return'])
plt.plot(result['benchmark_period_return'])
plt.legend()
plt.show()
