#!/usr/bin/env python3
"""
Enhanced AI Agent with Real AI Integration
Using Hugging Face's free API for better responses
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import os
import re
import json
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

class EnhancedAIAgent:
    """Enhanced AI agent with real AI capabilities using free APIs"""
    
    def __init__(self):
        self.conversation_history = []
        self.task_counter = 0
        self.start_time = time.time()
        
        # Hugging Face API (free tier)
        self.hf_api_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
        self.hf_token = os.getenv('HUGGINGFACE_TOKEN')  # Optional, works without token but with rate limits
        
        # Fallback responses for when API is unavailable
        self.fallback_responses = {
            'date_time': self._get_current_datetime,
            'greeting': lambda: "Hello! I'm an AI assistant ready to help you with questions and tasks.",
            'capabilities': lambda: "I can help with general questions, provide current date/time, assist with analysis, and engage in conversation. What would you like to know?",
            'default': lambda msg: f"I understand you're asking about '{msg}'. Let me help you with that. Could you provide more specific details?"
        }
        
    def _get_current_datetime(self):
        """Get current date and time"""
        now = datetime.now()
        return f"Today is {now.strftime('%A, %B %d, %Y')} and the current time is {now.strftime('%I:%M %p')}."
    
    def _call_huggingface_api(self, message):
        """Call Hugging Face API for AI responses"""
        try:
            headers = {}
            if self.hf_token:
                headers["Authorization"] = f"Bearer {self.hf_token}"
            
            payload = {"inputs": message}
            
            response = requests.post(
                self.hf_api_url, 
                headers=headers, 
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '').replace(message, '').strip()
            
            return None
            
        except Exception as e:
            print(f"Hugging Face API error: {e}")
            return None
    
    def _analyze_intent(self, message):
        """Analyze user intent for better responses"""
        message_lower = message.lower()
        
        # Date/time queries
        if any(word in message_lower for word in ['date', 'time', 'day', 'today', 'now', 'current']):
            return 'date_time'
            
        # Greetings
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return 'greeting'
            
        # Capability questions
        if any(word in message_lower for word in ['what can you', 'capabilities', 'what do you do', 'help']):
            return 'capabilities'
            
        return 'general'
    
    def _get_fallback_response(self, message, intent):
        """Get fallback response when AI API is unavailable"""
        if intent in self.fallback_responses:
            handler = self.fallback_responses[intent]
            if callable(handler):
                return handler() if intent != 'default' else handler(message)
        
        return self.fallback_responses['default'](message)
    
    def chat(self, message):
        """Enhanced chat with real AI integration"""
        intent = self._analyze_intent(message)
        
        # Handle specific intents locally
        if intent == 'date_time':
            return self._get_current_datetime()
        
        # Try AI API first
        ai_response = self._call_huggingface_api(message)
        
        if ai_response and len(ai_response.strip()) > 5:  # Valid AI response
            response = ai_response
            source = 'huggingface_ai'
        else:
            # Fallback to enhanced local responses
            response = self._get_fallback_response(message, intent)
            source = 'fallback_enhanced'
        
        # Store conversation history
        self.conversation_history.append({
            'timestamp': time.time(),
            'message': message,
            'intent': intent,
            'response': response[:200] + "..." if len(response) > 200 else response,
            'source': source
        })
        
        # Keep last 10 conversations
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
            
        return response
    
    def simulate_task_execution(self, task_description):
        """Enhanced task execution simulation"""
        self.task_counter += 1
        
        # Try to get AI insights for the task
        ai_insight = self._call_huggingface_api(f"How would you approach this task: {task_description}")
        
        current_time = self._get_current_datetime()
        
        result = f"""**Enhanced Task Analysis**

**Task**: {task_description}

**Current Context**: {current_time}

**AI Analysis**:
{ai_insight if ai_insight else "Analyzing task systematically..."}

**Recommended Approach**:
1. **Requirements Analysis**: Break down the task components
2. **Research Phase**: Gather relevant information and context
3. **Implementation Strategy**: Plan systematic execution
4. **Quality Assurance**: Validate results and ensure accuracy

**Next Steps**: 
For implementation, I recommend gathering specific requirements and available resources.

**Task ID**: enhanced_task_{self.task_counter}
**Status**: Analysis Complete
**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        return result
    
    def get_status(self):
        """Enhanced status information"""
        return {
            'agent_info': {
                'type': 'enhanced_ai_agent',
                'version': '2.0.0',
                'ai_integration': 'huggingface_api',
                'uptime_seconds': int(time.time() - self.start_time),
                'conversation_entries': len(self.conversation_history),
                'current_time': self._get_current_datetime()
            },
            'capabilities': {
                'real_ai_responses': True,
                'datetime_awareness': True,
                'intent_recognition': True,
                'task_analysis': True,
                'conversation_memory': True,
                'fallback_system': True
            },
            'api_status': {
                'huggingface_api': 'integrated',
                'fallback_system': 'active',
                'response_sources': ['ai_api', 'enhanced_fallback']
            }
        }

# Global enhanced agent instance
agent = EnhancedAIAgent()

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'agent_type': 'enhanced_ai_agent',
        'ai_integration': 'huggingface_api',
        'timestamp': time.time(),
        'uptime': int(time.time() - agent.start_time)
    })

@app.route('/status', methods=['GET'])
def status():
    """Get detailed status"""
    return jsonify(agent.get_status())

@app.route('/chat', methods=['POST'])
def chat():
    """Enhanced chat endpoint with real AI"""
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Message required'}), 400
    
    try:
        response = agent.chat(data['message'])
        return jsonify({
            'response': response,
            'text': response,
            'agent_type': 'Enhanced AI Assistant',
            'timestamp': time.time(),
            'current_datetime': agent._get_current_datetime(),
            'source': 'enhanced_ai_agent'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/execute-task', methods=['POST'])
def execute_task():
    """Task execution endpoint"""
    data = request.get_json()
    if not data or 'task' not in data:
        return jsonify({'error': 'Task description required'}), 400
    
    try:
        result = agent.simulate_task_execution(data['task'])
        return jsonify({
            'task_id': f'enhanced_task_{agent.task_counter}',
            'status': 'completed',
            'result': result,
            'response': result,  # Alternative field
            'execution_time': '< 100ms',
            'mode': 'simulation'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """Landing page"""
    return jsonify({
        'message': 'Enhanced AI Agent - Real AI Integration',
        'status': 'Running with real AI capabilities using Hugging Face API',
        'endpoints': {
            'GET /health': 'Health check',
            'GET /status': 'Detailed status',
            'POST /chat': 'Chat interface with real AI',
            'POST /execute-task': 'Task execution'
        },
        'optimization': 'Designed for dynamic AI interactions'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("🚀 Starting Enhanced AI Agent")
    print(f"🌐 Running on port {port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)