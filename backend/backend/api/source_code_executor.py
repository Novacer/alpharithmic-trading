from rest_framework.views import APIView
from rest_framework.response import Response
import os

from ..algorithms.custom_algos.template_algorithm import template_algorithm


class GetDefaultSourceCodeFile(APIView):
    def get(self, request, format=None):
        file_name = os.path.join(os.path.dirname(__file__), '..', 'algorithms', 'example_algorithm.py')
        with open(file_name) as file:
            code = file.read()
            json = {'code': code}
            return Response(json)


class ExecuteSourceCode(APIView):
    def post(self, request, format=None):
        json = template_algorithm(request.data['src_code'],
                                  request.data['capital_base'],
                                  request.data['start'],
                                  request.data['end'],
                                  request.data['log_channel'])
        return Response(json)

