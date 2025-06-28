#!/usr/bin/env python3
"""
Express-compatible API wrapper for the Autonomous AI Agent
Provides REST endpoints for integration with Express applications
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import threading
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autonomous_agent import AutonomousAgent

app = Flask(__name__)
CORS(app)  # Enable CORS for Express integration

# Global agent instance
agent = None
agent_lock = threading.Lock()

def initialize_agent():
    """Initialize the agent with fallback to free Ollama"""
    global agent
    try:
        # Try Ollama first (free)
        agent = AutonomousAgent(model_type="ollama", model_name="llama3")
        print("✅ Agent initialized with Ollama (FREE)")
        return True
    except Exception as e:
        print(f"❌ Ollama failed: {e}")
        try:
            # Fallback to OpenAI if configured
            agent = AutonomousAgent(model_type="openai", model_name="gpt-4")
            print("✅ Agent initialized with OpenAI")
            return True
        except Exception as e2:
            print(f"❌ Both models failed. Ollama: {e}, OpenAI: {e2}")
            return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'agent_ready': agent is not None,
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
            'timestamp': time.time()
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

@app.route('/memories', methods=['GET'])
def get_memories():
    """Get agent memories"""
    if not agent:
        return jsonify({'error': 'Agent not initialized'}), 500
    
    memory_type = request.args.get('type')  # 'short_term' or 'long_term'
    limit = int(request.args.get('limit', 10))
    
    try:
        with agent_lock:
            memories = agent.memory.retrieve_memories(memory_type, limit)
        
        return jsonify([{
            'id': m.id,
            'type': m.type,
            'content': m.content,
            'context': m.context,
            'timestamp': m.timestamp.isoformat(),
            'importance': m.importance
        } for m in memories])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Autonomous Agent API Server")
    print("=" * 50)
    
    # Initialize agent
    if initialize_agent():
        print(f"🌐 Starting Flask server on http://localhost:5000")
        print("📡 Endpoints available:")
        print("  GET  /health          - Health check")
        print("  POST /chat            - General chat")
        print("  POST /execute-task    - Execute autonomous tasks")
        print("  GET  /status          - Agent status")
        print("  GET  /memories        - Retrieve memories")
        print("\n💡 Ready for Express integration!")
        
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    else:
        print("❌ Failed to initialize agent. Please check Ollama installation.")
        sys.exit(1)