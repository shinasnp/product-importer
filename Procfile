web: daphne product_importer.asgi:application --port $PORT --bind 0.0.0.0
worker: celery -A product_importer worker --without-heartbeat --without-gossip --without-mingle
