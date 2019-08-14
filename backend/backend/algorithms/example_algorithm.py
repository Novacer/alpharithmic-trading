# Zipline API (https://www.zipline.io/appendix.html)
from zipline.api import order, symbol, schedule_function
from zipline.utils.events import date_rules


# initialize "global" variables and schedule actions
# you can set context.anything_you_want, and this field will be available for access in other functions
# functions scheduled in init take context and data parameters
def initialize(context):
    context.shares_per_day = 10
    schedule_function(func=buy_apple_shares, date_rule=date_rules.every_day())

def before_trading_start(context, data):
    pass


# buy 10 apple shares every day
def buy_apple_shares(context, data):
    order(symbol('AAPL'), context.shares_per_day)
