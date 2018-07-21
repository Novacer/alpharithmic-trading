from rest_framework.views import APIView
from rest_framework.response import Response
from ..algorithms.validation import validate_single_stock


class Validate(APIView):
    def get(self, request, format=None):

        ticker = request.query_params.get('symbol')
        result = validate_single_stock(ticker)

        if result:
            json = {
                'success': True,
                'message': 'Symbol was found in database'
            }

            return Response(json)
        else:
            json = {
                'success': False,
                'message': 'No such symbol in database'
            }

            return Response(json)

