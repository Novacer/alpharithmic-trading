from rest_framework.views import APIView
from rest_framework.response import Response
import django_rq
from rq.job import Job

def f(x, y):
    return x + y


class HelloWorld(APIView):
    def get(self, request, format=None):
        queue = django_rq.get_queue('high')
        job = queue.enqueue(f, 1, 2)

        return Response({'success': True, 'job_id': job.key})


class PostWorld(APIView):
    def post(self, request, format=None):

        connection = django_rq.get_connection('high')

        thing = Job.fetch(request.data['job_id'], connection)

        return Response({'success': True, 'content': 'Hello World ' + str(thing.result)})
