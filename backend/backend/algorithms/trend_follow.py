import numpy as np
import pandas as pd
import statsmodels.api as sm
from zipline.api import attach_pipeline, pipeline_output, schedule_function
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
            (b , a) = results.params

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

                # Long but slope turns down, then exit
                if context.weights[s] > 0 and slope < 0:
                    context.weights[s] = 0

                # Short but slope turns up
                elif context.weights < 0 and slope > 0:
                    context.weights[s] = 0

                # Profit take reaches top 95% bollinger band
                if delta[-1] > context.profittake * sd and s in context.weights and context.weights[s] > 0:
                    context.weights[s] = 0

            else:

                # Trend is up and price crosses the regression line
                if slope > slope_min and delta[-1] > 0 and delta[-2] < 0 and dd < context.maxdrawdown:
                    context.weights[s] = slope
                    context.drawdown[s] = slope_min

                # Trend is down and price crosses the regression line
                if slope < -slope_min and delta[-1] < 0 and delta[-2] > 0  and dd < context.maxdrawdown:
                    context.weights[s] = slope
                    context.drawdown[s] = slope_min

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