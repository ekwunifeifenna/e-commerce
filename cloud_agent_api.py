#!/usr/bin/env python3
"""
Cloud-optimized API wrapper for Render deployment
Uses OpenAI with fallback to a simple mock agent for demo purposes
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import threading
import time
import json
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)  # Enable CORS for Express integration

# Global agent instance
agent = None
agent_lock = threading.Lock()

class MockAgent:
    """Mock agent for demo purposes when no real LLM is available"""
    
    def __init__(self):
        self.model_type = "mock"
        self.model_name = "demo-agent"
        
    def chat(self, message: str) -> str:
        """Simple mock chat responses"""
        responses = {
            "hello": "Hello! I'm a demo AI agent. For full functionality, please set up OpenAI API key.",
            "help": "I can help with basic responses. Available commands: hello, help, status, demo",
            "status": "I'm running in demo mode. Set OPENAI_API_KEY environment variable for full AI capabilities.",
            "demo": "This is a demonstration of the autonomous AI agent API. It can perform tasks, maintain memory, and integrate with your Express app."
        }
        
        message_lower = message.lower()
        for keyword, response in responses.items():
            if keyword in message_lower:
                return response
                
        return f"Demo response: I received your message '{message}'. For full AI capabilities, please configure OpenAI API key in environment variables."
    
    def execute_task(self, task_description: str, priority: int = 5) -> dict:
        """Mock task execution"""
        return {
            'task_id': f"demo_task_{int(time.time())}",
            'status': 'completed',
            'result': f"Demo result: This is a simulated completion of the task '{task_description}'. In full mode, the AI would break this down into subtasks and execute them autonomously.",
            'attempts': 1
        }
    
    def get_status(self) -> dict:
        """Mock status"""
        return {
            'agent_info': {
                'model_type': self.model_type,
                'model_name': self.model_name,
                'current_task': None,
                'mode': 'demo'
            },
            'cost_summary': {},
            'task_statistics': {'completed': 5, 'demo': 1},
            'memory_entries': 0
        }

def initialize_agent():
    """Initialize agent with cloud-friendly fallbacks"""
    global agent
    
    # Try OpenAI first if API key is available
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key and openai_key != 'your_openai_api_key_here':
        try:
            from autonomous_agent import AutonomousAgent
            agent = AutonomousAgent(model_type="openai", model_name="gpt-4")
            print("✅ Agent initialized with OpenAI GPT-4")
            return True
        except Exception as e:
            print(f"❌ OpenAI initialization failed: {e}")
    
    # Fallback to mock agent for demonstration
    print("🔄 Using mock agent for demonstration")
    print("💡 Set OPENAI_API_KEY environment variable for full AI capabilities")
    agent = MockAgent()
    return True

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'agent_ready': agent is not None,
        'agent_type': getattr(agent, 'model_type', 'unknown'),
        'timestamp': time.time()
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint for general conversations"""
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 500
    
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Message required'}), 400
    
    message = data['message']
    
    try:
        with agent_lock:
            response = agent.chat(message)
        
        return jsonify({
            'response': response,
            'timestamp': time.time(),
            'agent_type': getattr(agent, 'model_type', 'unknown')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/execute-task', methods=['POST'])
def execute_task():
    """Execute autonomous task endpoint"""
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 500
    
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({'error': 'Task description required'}), 400
    
    task_description = data['task']
    priority = data.get('priority', 5)
    
    try:
        with agent_lock:
            result = agent.execute_task(task_description, priority)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def get_status():
    """Get agent status and statistics"""
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 500
    
    try:
        with agent_lock:
            status = agent.get_status()
        
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/demo', methods=['GET'])
def demo_endpoint():
    """Demo endpoint to test the API"""
    return jsonify({
        'message': 'Autonomous AI Agent API is running!',
        'endpoints': {
            'POST /chat': 'General conversation',
            'POST /execute-task': 'Execute autonomous tasks', 
            'GET /status': 'Agent status',
            'GET /health': 'Health check',
            'GET /demo': 'This demo endpoint'
        },
        'agent_type': getattr(agent, 'model_type', 'unknown'),
        'timestamp': time.time()
    })

# For cloud platforms, we need to handle the port from environment
if __name__ == '__main__':
    print("🚀 Starting Cloud-Optimized AI Agent API")
    print("=" * 50)
    
    # Initialize agent
    if initialize_agent():
        # Get port from environment (Render sets this automatically)
        port = int(os.getenv('PORT', 5000))
        
        print(f"🌐 Starting server on port {port}")
        print("📡 Endpoints available:")
        print("  GET  /health          - Health check")
        print("  POST /chat            - General chat")
        print("  POST /execute-task    - Execute autonomous tasks")
        print("  GET  /status          - Agent status")
        print("  GET  /demo            - Demo endpoint")
        print("\n💡 Ready for cloud deployment!")
        
        # Use 0.0.0.0 to accept connections from anywhere (required for cloud platforms)
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
    else:
        print("❌ Failed to initialize agent")
        sys.exit(1)