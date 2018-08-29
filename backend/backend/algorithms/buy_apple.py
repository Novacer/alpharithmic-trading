# Zipline API
from zipline.api import order, symbol
from zipline import run_algorithm

# Data frames
import pandas as pd

# Logging
from websocket import create_connection

from ..api.create_response import create_json_response


def apple_run(shares_per_day, capital_base, start_date, end_date, log_channel):

    ws = create_connection("ws://alpharithmic.herokuapp.com/ws/logs/%s/" % log_channel)
    msg_placeholder = "{\"message\": \"%s\"}"

    ws.send(msg_placeholder % "Link Start")

    def init(context):
        ws.send(msg_placeholder % "Simulation Start")
        pass

    def handle(context, data):
        order(symbol('AAPL'), shares_per_day)
        ws.send(msg_placeholder % ("Ordered %s shares of Apple" % str(shares_per_day)))

    start = pd.to_datetime(start_date).tz_localize('US/Eastern')
    end = pd.to_datetime(end_date).tz_localize('US/Eastern')
    result = run_algorithm(start, end, capital_base=capital_base,
                           initialize=init,
                           handle_data=handle,
                           bundle="quantopian-quandl")

    ws.send(msg_placeholder % "Simulation End")
    ws.send(msg_placeholder % "Fetching backtest results from Redis Queue...")

    result.dropna(inplace=True)

    ws.close()

    return create_json_response(result)
