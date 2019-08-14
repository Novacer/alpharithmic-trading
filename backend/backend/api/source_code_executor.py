from rest_framework.views import APIView
from rest_framework.response import Response
import os


class GetDefaultSourceCodeFile(APIView):
    def get(self, request, format=None):
        file_name = os.path.join(os.path.dirname(__file__), '..', 'algorithms', 'example_algorithm.py')
        with open(file_name) as file:
            code = file.read()
            json = {'code': code}
            return Response(json)
