from zipline.api import order, record, symbol
from zipline import run_algorithm
import pandas as pd


def apple_run(shares_per_day, capital_base, start_date, end_date):

    def init(context):
        pass

    def handle(context, data):
        order(symbol('AAPL'), shares_per_day)
        record(AAPL=data.current(symbol('AAPL'), 'price'))

    start = pd.to_datetime(start_date).tz_localize('US/Eastern')
    end = pd.to_datetime(end_date).tz_localize('US/Eastern')
    result = run_algorithm(start, end, capital_base=capital_base,
                           initialize=init,
                           handle_data=handle,
                           bundle="quantopian-quandl")

    result.dropna(inplace=True)

    return result
