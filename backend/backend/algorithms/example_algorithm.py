# Zipline API (https://www.zipline.io/appendix.html)
from zipline.api import order, symbol, schedule_function
from zipline.utils.events import date_rules


# initialize "global" variables and schedule actions
# you can set context.anything_you_want, and this field will be available for access in other functions
# functions scheduled in init take context and data parameters
def initialize(context):
    context.shares_per_day = 10
    context.day = 0
    schedule_function(func=buy_or_sell_apple_shares, date_rule=date_rules.every_day())


# do action before the trading day starts
def before_trading_start(context, data):
    context.day += 1


# alternate between buying and selling AAPL everyday
def buy_or_sell_apple_shares(context, data):
    if context.day % 2 == 1:
        # buy stock
        order(symbol('AAPL'), context.shares_per_day)

    else:
        # sell stock
        order(symbol('AAPL'), -context.shares_per_day)