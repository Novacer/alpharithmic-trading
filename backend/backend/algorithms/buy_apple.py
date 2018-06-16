from zipline.api import order, record, symbol
from zipline import run_algorithm
import pandas as pd
import matplotlib.pyplot as plt
import mpld3 as mp


def initialize(context):
    pass


def handle_data(context, data):
    order(symbol('AAPL'), 10)
    record(AAPL=data.current(symbol('AAPL'), 'price'))


def run():
    start = pd.to_datetime('2015-01-01').tz_localize('US/Eastern')
    end = pd.to_datetime('2016-01-01').tz_localize('US/Eastern')
    result = run_algorithm(start, end, capital_base=100000,
                           initialize=initialize,
                           handle_data=handle_data, bundle="quandl")

    return result


data = run()
data.dropna(inplace=True)

print(data.head())

plt.plot(data['benchmark_period_return'])

fig = plt.gcf()

print(mp.fig_to_html(fig))

