from scipy import stats
import pandas as pd
from zipline.pipeline import Pipeline
from zipline.api import attach_pipeline, pipeline_output, schedule_function, order
from zipline.pipeline.factors import AverageDollarVolume
from zipline.utils.events import date_rules
from zipline import run_algorithm
from websocket import create_connection


def mean_rev_run(start_date, end_date, capital_base, shares, log_channel):

    ws = create_connection("ws://alpharithmic.herokuapp.com/ws/logs/%s/" % log_channel)
    msg_placeholder = "{\"message\": \"%s\"}"

    ws.send(msg_placeholder % "Link Start")

    def initialize(context):
        ws.send(msg_placeholder % "Simulation Start")

        pipe = Pipeline()
        attach_pipeline(pipe, "volume_pipeline")

        # 100 day average dollar volume factor
        dollar_volume = AverageDollarVolume(window_length=100)
        pipe.add(dollar_volume, "100_day_dollar_volume")

        # filter out only the top stocks by dollar volume
        high_dollar_volume = dollar_volume.percentile_between(99, 100)
        pipe.set_screen(high_dollar_volume)

        # set the global variables
        context.dev_multiplier = 2
        context.max_notional = 1000000
        context.min_notional = -1000000
        context.days_traded = 0

        ws.send(msg_placeholder % "Pipeline filter attached")

        schedule_function(func=choose_and_order, date_rule=date_rules.every_day())

    def before_trading_start(context, data):
        output = pipeline_output("volume_pipeline")

        sort_by_liquidity = output.sort("100_day_dollar_volume", ascending=False)

        context.my_securities = sort_by_liquidity.index

    def choose_and_order(context, data):
        context.days_traded += 1

        dev_mult = context.dev_multiplier
        notional = context.portfolio.positions_value

        linear = get_linear(context, data)

        # check every 20 days
        if context.days_traded % 20 == 0:
            try:
                for stock in context.my_securities:
                    close = data.current(stock, "close")
                    moving_avg = linear[stock]
                    stddev_history = data.history(stock, "price", 20, "1d")[:-1]
                    moving_dev = stddev_history.std()

                    high_band = moving_avg + dev_mult * moving_dev
                    low_band = moving_avg - dev_mult * moving_dev

                    if close > high_band and notional > context.min_notional:
                        order(stock, -shares)
                        ws.send(msg_placeholder % ("Shorted " + str(shares) + " of " + str(stock)))

                    elif close < low_band and notional < context.max_notional:
                        order(stock, shares)
                        ws.send(msg_placeholder % ("Bought " + str(shares) + " of " + str(stock)))
            except:
                return

    def get_linear(context, data):
        days = [i for i in range(1, 21)]  # list comprehension
        stocks = {}
        for stock in context.my_securities:
            linear = stats.linregress(days, data.history(stock, "price", 20, "1d"))[1]
            stocks[stock] = linear
        return stocks

    start = pd.to_datetime(start_date).tz_localize('US/Eastern')
    end = pd.to_datetime(end_date).tz_localize('US/Eastern')

    result = run_algorithm(start, end,
                           initialize=initialize, before_trading_start=before_trading_start,
                           capital_base=capital_base,
                           bundle="quantopian-quandl")

    ws.send(msg_placeholder % "Simulation End")
    ws.close()

    result.dropna(inplace=True)

    return result