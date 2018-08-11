import matplotlib
matplotlib.use("Agg")
from rest_framework.views import APIView
from rest_framework.response import Response
from ..algorithms.buy_apple import apple_run
from ..algorithms.mean_reversion import mean_rev_run
from ..algorithms.random_forest_regression import rfr_run
from ..algorithms.rsi_divergence import rsi_div_run
import django_rq


class BuyAppleResult(APIView):
    def post(self, request, format=None):

        queue = django_rq.get_queue('high')

        job = queue.enqueue(apple_run,
                            request.data['shares'],
                            request.data['capital_base'],
                            request.data['start'],
                            request.data['end'],
                            request.data['log_channel'])

        json = {
            'success': True,
            'job_id': job.key
        }

        return Response(json)


class MeanReversionResult(APIView):
    def post(self, request, format=None):

        queue = django_rq.get_queue('high')

        job = queue.enqueue(mean_rev_run,
                            request.data['start'],
                            request.data['end'],
                            request.data['capital_base'],
                            request.data['shares'],
                            request.data['log_channel'])

        json = {
            'success': True,
            'job_id': job.key
        }

        return Response(json)


class RandomForestRegressionResult(APIView):
    def post(self, request, format=None):

        queue = django_rq.get_queue('high')

        job = queue.enqueue(rfr_run,
                            request.data['start'],
                            request.data['end'],
                            request.data['capital_base'],
                            request.data['ticker'],
                            request.data['minutes'],
                            request.data['log_channel'])

        json = {
            'success': True,
            'job_id': job.key
        }

        return Response(json)


class RsiDivergenceResult(APIView):
    def post(self, request, format=None):

        queue = django_rq.get_queue('high')

        job = queue.enqueue(rsi_div_run,
                            request.data['start'],
                            request.data['end'],
                            request.data['capital_base'],
                            request.data['ticker'],
                            request.data['log_channel'])

        json = {
            'success': True,
            'job_id': job.key
        }

        return Response(json)


class GetResult(APIView):
    def post(self, request, format=None):
        queue = django_rq.get_queue('high')

        job = queue.fetch_job(request.data['job_id'])

        if job is None or job.result is None:
            return Response({'done': False})

        else:
            response = Response(job.result)
            job.delete()
            return response
