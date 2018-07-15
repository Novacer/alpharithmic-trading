import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpld3 as mp


def create_json_response(result):
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

    plt.close(1)  # clear the memory
    plt.close(2)  # clear the memory

    final_alpha = result['alpha'].iloc[-1]

    json = {
        "done": True,
        "alpha": final_alpha,
        "algo_to_benchmark": algo_result,
        "rolling_beta": beta_result
    }

    return json
