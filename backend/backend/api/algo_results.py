from rest_framework.views import APIView
from rest_framework.response import Response
from ..algorithms.buy_apple import apple_run
from ..algorithms.mean_reversion import mean_rev_run
import matplotlib.pyplot as plt
import mpld3 as mp


class BuyAppleResult(APIView):
    def post(self, request, format=None):
        result = apple_run(request.data['shares'],
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

        algo_result = mp.fig_to_dict(algo_to_bench_fig)
        beta_result = mp.fig_to_dict(beta_fig)

        final_alpha = result['alpha'].iloc[-1]

        json = {"alpha": final_alpha,
                "algo_to_benchmark": algo_result,
                "rolling_beta": beta_result}

        return Response(json)


class MeanReversionResult(APIView):
    def post(self, request, format=None):
        result = mean_rev_run(request.data['start'],
                              request.data['end'],
                              request.data['capital_base'])

        plt.figure(1)
        plt.plot(result['algorithm_period_return'])
        plt.plot(result['benchmark_period_return'])

        algo_to_bench_fig = plt.gcf()

        plt.figure(2)
        plt.plot(result['beta'])

        beta_fig = plt.gcf()

        atb_html = mp.fig_to_html(algo_to_bench_fig, no_extras=True, template_type='simple', figid="fig_1")
        beta_html = mp.fig_to_html(beta_fig, no_extras=True, template_type='simple', figid="fig_2")

        final_alpha = result['alpha'].iloc[-1]

        json = {"alpha": final_alpha,
                "algo_to_benchmark": atb_html,
                "rolling_beta": beta_html}

        return Response(json)