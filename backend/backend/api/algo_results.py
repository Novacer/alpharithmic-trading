from rest_framework.views import APIView
from rest_framework.response import Response
from ..algorithms.buy_apple import run
import matplotlib.pyplot as plt
import mpld3 as mp


class BuyAppleResult(APIView):
    def post(self, request, format=None):
        result = run(request.data['shares'],
                     request.data['capital_base'],
                     request.data['start'],
                     request.data['end'])

        plt.figure(1)
        plt.plot(result['algorithm_period_return'])
        plt.plot(result['benchmark_period_return'])

        algo_to_bench_fig = plt.gcf()

        plt.figure(2)
        plt.plot(result['beta'])

        beta_fig = plt.gcf()

        atb_html = mp.fig_to_html(algo_to_bench_fig)
        beta_html = mp.fig_to_html(beta_fig)

        final_alpha = result['alpha'].iloc[-1]

        json = {"alpha": final_alpha,
                "figures": [atb_html, beta_html]}

        return Response(json)
