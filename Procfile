# Render deployment configuration
# This file tells Render how to build and run your application

web: gunicorn --bind 0.0.0.0:$PORT --timeout 30 --workers 1 --max-requests 1000 --max-requests-jitter 100 app:app