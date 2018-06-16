from rest_framework.views import APIView
from rest_framework.response import Response


class HelloWorld(APIView):
    def get(self, request, format=None):
        return Response({'success': True, 'content': 'Hello World'})


class PostWorld(APIView):
    def post(self, request, format=None):
        return Response({'success': True, 'content': 'Hello World ' + request.data['username']})
