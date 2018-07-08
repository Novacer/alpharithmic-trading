from rest_framework.views import APIView
from rest_framework.response import Response
from ..algorithms.buy_apple import apple_run
from ..algorithms.mean_reversion import mean_rev_run
from ..algorithms.random_forest_regression import rfr_run
import matplotlib.pyplot as plt
import mpld3 as mp


class BuyAppleResult(APIView):
    def post(self, request, format=None):
        print(request.data['start'])
        result = apple_run(request.data['shares'],
                           request.data['capital_base'],
                           request.data['start'],
                           request.data['end'])

        dates = result.index.values.tolist()

        result['unix'] = dates
        result['unix'] = result['unix'].divide(1000000)

        result.set_index('unix', inplace=True)

        plt.figure(1)
        plt.plot(result['algorithm_period_return'])
        plt.plot(result['benchmark_period_return'])
        plt.legend()

        algo_to_bench_fig = plt.gcf()

        plt.figure(2)
        plt.plot(result['beta'])
        plt.legend()

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

        dates = result.index.values.tolist()

        result['unix'] = dates
        result['unix'] = result['unix'].divide(1000000)

        result.set_index('unix', inplace=True)

        plt.figure(1)
        plt.plot(result['algorithm_period_return'])
        plt.plot(result['benchmark_period_return'])
        plt.legend()

        algo_to_bench_fig = plt.gcf()

        plt.figure(2)
        plt.plot(result['beta'])
        plt.legend()

        beta_fig = plt.gcf()

        algo_result = mp.fig_to_dict(algo_to_bench_fig)
        beta_result = mp.fig_to_dict(beta_fig)

        final_alpha = result['alpha'].iloc[-1]

        json = {"alpha": final_alpha,
                "algo_to_benchmark": algo_result,
                "rolling_beta": beta_result}

        return Response(json)


class RandomForestRegressionResult(APIView):
    def post(self, request, format=None):
        result = rfr_run(request.data['start'],
                         request.data['end'],
                         request.data['capital_base'],
                         request.data['ticker'])

        dates = result.index.values.tolist()

        result['unix'] = dates
        result['unix'] = result['unix'].divide(1000000)

        result.set_index('unix', inplace=True)

        plt.figure(1)
        plt.plot(result['algorithm_period_return'])
        plt.plot(result['benchmark_period_return'])
        plt.legend()

        algo_to_bench_fig = plt.gcf()

        plt.figure(2)
        plt.plot(result['beta'])
        plt.legend()

        beta_fig = plt.gcf()

        algo_result = mp.fig_to_dict(algo_to_bench_fig)
        beta_result = mp.fig_to_dict(beta_fig)

        final_alpha = result['alpha'].iloc[-1]

        json = {
            "alpha": final_alpha,
            "algo_to_benchmark": algo_result,
            "rolling_beta": beta_result
        }

        return Response(json)
