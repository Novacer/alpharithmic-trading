from zipline.api import symbol
from zipline import run_algorithm
import pandas as pd


def validate_single_stock(ticker):

    def init(context):
        symbol(ticker)

    def handle_data(context, data):
        pass

    start = pd.to_datetime("2017-01-09").tz_localize('US/Eastern')
    end = pd.to_datetime("2017-01-11").tz_localize('US/Eastern')

    try:
        run_algorithm(start, end, capital_base=1000000,
                      initialize=init,
                      handle_data=handle_data,
                      bundle="quandl")

        return True
    except:
        return False

