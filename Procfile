web: daphne backend.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python backend.manage.py runworker channels -v2
