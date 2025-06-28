#!/usr/bin/env python3
"""
Simple app.py wrapper for Render deployment
Imports the Flask app from cloud_agent_api.py
"""

from cloud_agent_api import app

if __name__ == '__main__':
    app.run()