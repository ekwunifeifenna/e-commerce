"""
App entry point for deployment compatibility
Imports the Flask app from autonomous_agent.py
"""

from autonomous_agent import app

if __name__ == "__main__":
    app.run()