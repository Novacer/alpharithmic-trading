# initialize "global" variables and schedule actions
# you can set context.anything_you_want, and this field will be available for access in other functions
# functions scheduled in init take context and data parameters
def initialize(context):
    context.shares_per_transaction = 10
    context.day = 0


# before_trading_start gets called before every trading day
def before_trading_start(context, data):
    context.day = context.day + 1


# handle_data gets called once for every data point in the date range
# if data is by the minute, then handle_data is called every minute
# if data is by the hour, then handle_data is called every hour etc
# alternate between buying and selling AAPL every day
def handle_data(context, data):
    if context.day % 2 == 1:
        # buy stock
        order(symbol('AAPL'), context.shares_per_transaction)

    else:
        # sell stock
        order(symbol('AAPL'), -context.shares_per_transaction)
