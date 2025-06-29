# Render deployment configuration
# This file tells Render how to build and run your application

web: gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 1 autonomous_agent:app