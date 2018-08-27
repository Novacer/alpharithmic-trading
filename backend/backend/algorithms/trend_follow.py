import numpy as np
import pandas as pd
import statsmodels.api as sm
from zipline.api import attach_pipeline, pipeline_output, schedule_function, get_open_orders, order_target_percent
from zipline.pipeline import Pipeline
from zipline.utils.events import date_rules, time_rules
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

        schedule_function(stop_loss, date_rules.every_day(), time_rules.market_open(minutes=30))
        schedule_function(regression, date_rules.every_day(), time_rules.market_open(minutes=50))
        schedule_function(trade, date_rules.every_day(), time_rules.market_open(minutes=100))

        for thirty_minute_interval in range(30, 391, 30):
            schedule_function(execute_transactions, date_rules.every_day,
                              time_rules.market_open(minutes=thirty_minute_interval))  # execute every 30 minutes

        attach_pipeline(create_high_dollar_volume_pipeline(), 'top_dollar_volume')


    def create_high_dollar_volume_pipeline():
        pipe = Pipeline()

        dollar_volume = AverageDollarVolume(window_length=63)  # 63 days = 1 quarter
        pipe.add(dollar_volume, 'dollar_volume')

        high_dollar_volume = dollar_volume.percentile_between(95, 100)  # top 5% by dollar volume
        pipe.set_screen(high_dollar_volume)

        return pipe

    def before_trading_start(context, data):
        context.pipe_output = pipeline_output('top_dollar_volume')

        context.security_list = context.pipe_output.index

    def regression(context, data):
        prices = data.history(context.security_list, 'open', context.lookback, '1d')

        X = range(len(prices))

        # Add constant to ensure intercept
        A = sm.add_constant(X)

        for s in context.security_list:

            # Price movement standard deviation
            sd = prices[s].std()

            # Price points to run regression
            Y = prices[s].values

            if np.isnan(Y).any():
                continue

            # y = ax + b
            results = sm.OLS(Y, A).fit()
            (b, a) = results.params

            slope = a / Y[-1] * 252  # Daily return regression * 1 year

            global dd

            if slope > 0:
                dd = drawdown(Y)
            elif slope < 0:
                dd = drawdown(-Y)

            # How far are we from regression line?
            delta = Y - (np.dot(a, X) + b)

            slope_min = max(dd, context.minimum_return)

            gain = get_gain(context, s)

            # Exit
            if context.weights[s] != 0 and s in context.weights:

                # Long but slope turns down
                if context.weights[s] > 0 and slope < 0:
                    context.weights[s] = 0

                # Short but slope turns up
                elif context.weights < 0 and slope > 0:
                    context.weights[s] = 0

                # Profit take reaches top 95% bollinger band
                elif delta[-1] > context.profittake * sd and s in context.weights and context.weights[s] > 0:
                    context.weights[s] = 0

            # Enter
            else:

                # Trend is up and price crosses the regression line
                if slope > slope_min and delta[-1] > 0 and delta[-2] < 0 and dd < context.maxdrawdown:
                    context.weights[s] = slope
                    context.drawdown[s] = slope_min

                # Trend is down and price crosses the regression line
                if slope < -slope_min and delta[-1] < 0 and delta[-2] > 0  and dd < context.maxdrawdown:
                    context.weights[s] = slope
                    context.drawdown[s] = slope_min

    def execute_transactions(context, data):
        open_orders = get_open_orders()

        for s in context.shares:
            if not data.can_trade(s) or s in open_orders:
                continue

            order_target_percent(s, context.shares[s])

    def trade(context, data):
        weights = context.weights

        positions = sum(weights[weight] != 0 for weight in weights)
        held_positions = [p for p in context.portfolio.positions if context.portfolio.positions[p].amount != 0]

        context.securities = context.security_list.tolist() + held_positions

        for security in context.securities:

            if security not in weights:
                context.shares.pop(security, 0)
                context.drawdown.pop(security, 0)

            elif weights[security] == 0:
                context.shares.pop(security, 0)
                context.drawdown.pop(security, 0)

            elif weights[security] > 0:
                context.shares[security] = context.max_leverage / positions

            elif weights[security] < 0:
                context.shares[security] = -(context.max_leverage / positions)

    def stop_loss(context, data):

        prices = data.history(context.portfolio.positions.keys(), 'price', context.lookback, '1d')

        for s in context.portfolio.positions:

            if context.weights[s] == 0 or s not in context.weights:
                context.shares[s] = 0
                continue

            if s not in prices or s in get_open_orders():
                continue

            gain = get_gain(context, s)

            if context.portfolio.positions[s].amount > 0 and drawdown(prices[s].values) > context.drawdown[s]:
                context.weights[s] = 0
                context.shares[s] = 0  # stop loss

            elif context.portfolio.positions[s].amount < 0 and drawdown(- prices[s].values) > context.drawdown[s]:
                context.weights[s] = 0
                context.shares[s] = 0

    def drawdown(xs):
        if len(xs) == 0:
            return 0

        period_end = np.argmax(np.maximum.accumulate(xs) - xs)

        if len(xs[:period_end]) == 0:
            return 0

        period_start = np.argmax(xs[:period_end])
        return abs((xs[period_start] - xs[period_end])/ xs[period_end])

    def get_gain(context, s):

        gain = 0

        if s in context.portfolio.positions:
            cost = context.portfolio.positions[s].cost_basis
            amount = context.portfolio.positions[s].amount
            price = context.portfolio.positions[s].last_sale_price

            if cost == 0:
                return 0

            if amount > 0:
                gain = price / cost - 1

            elif amount < 0:
                gain = 1 - price / cost

        return gain