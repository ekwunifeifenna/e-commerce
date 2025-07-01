#!/usr/bin/env python3
"""
Lightweight AI Agent - Render Free Tier Optimized
Memory usage: ~50-80MB (well within 512MB limit)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import os
import re
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

class LightweightAIAgent:
    """Memory-optimized AI agent using pattern matching instead of LLM"""
    
    def __init__(self):
        self.conversation_history = []
        self.task_counter = 0
        self.start_time = time.time()
        
        # Lightweight knowledge base
        self.knowledge_base = {
            'greetings': [
                "Hello! I'm your AI assistant. How can I help you today?",
                "Hi there! I'm ready to assist you with various tasks.",
                "Welcome! I can help with analysis, research, and general questions."
            ],
            'capabilities': [
                "I can help with data analysis and research",
                "I provide structured responses and task breakdowns", 
                "I assist with e-commerce, healthcare, and technical questions",
                "I can simulate task execution and provide detailed reports"
            ],
            'aba_therapy': [
                "For ABA therapy questions, I recommend consulting with licensed BCBAs",
                "ABA best practices include data-driven interventions and regular progress monitoring",
                "Documentation should follow current ethical guidelines and standards"
            ],
            'billing': [
                "For billing questions, I can provide general guidance on healthcare billing practices",
                "Claims processing typically involves verification, coding, and submission",
                "Always ensure compliance with current billing regulations"
            ],
            'technical': [
                "I can help with technical analysis and troubleshooting approaches",
                "For complex issues, I recommend breaking them into smaller components",
                "Documentation and systematic testing are key to resolution"
            ]
        }
        
    def analyze_intent(self, message):
        """Lightweight intent analysis using keyword matching"""
        message_lower = message.lower()
        
        # Greeting detection
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return 'greeting'
            
        # Capability inquiry
        if any(word in message_lower for word in ['what can you do', 'capabilities', 'help']):
            return 'capabilities'
            
        # Domain-specific intents
        if any(word in message_lower for word in ['aba', 'therapy', 'clinical', 'bcba']):
            return 'aba_therapy'
            
        if any(word in message_lower for word in ['billing', 'claims', 'insurance', 'payment']):
            return 'billing'
            
        if any(word in message_lower for word in ['technical', 'error', 'bug', 'troubleshoot']):
            return 'technical'
            
        # Task execution keywords
        if any(word in message_lower for word in ['analyze', 'research', 'task', 'execute']):
            return 'task_execution'
            
        return 'general'
    
    def generate_response(self, message, intent):
        """Generate contextual response based on intent"""
        
        if intent == 'greeting':
            return self.knowledge_base['greetings'][0]
            
        elif intent == 'capabilities':
            return "I'm a lightweight AI assistant with these capabilities:\n\n" + "\n".join(f"• {cap}" for cap in self.knowledge_base['capabilities'])
            
        elif intent == 'aba_therapy':
            base_response = self.knowledge_base['aba_therapy'][0]
            return f"{base_response}\n\nFor specific ABA guidance with your query: '{message}', I recommend:\n• Consulting current research\n• Following ethical guidelines\n• Documenting interventions thoroughly"
            
        elif intent == 'billing':
            return f"Regarding billing: {self.knowledge_base['billing'][0]}\n\nFor your specific question about '{message}', consider:\n• Reviewing current regulations\n• Verifying coding accuracy\n• Ensuring proper documentation"
            
        elif intent == 'technical':
            return f"For technical assistance: {self.knowledge_base['technical'][0]}\n\nRegarding '{message}':\n• Break down the problem\n• Check documentation\n• Test systematically"
            
        elif intent == 'task_execution':
            return self.simulate_task_execution(message)
            
        else:
            return f"I understand you're asking about: '{message}'\n\nI can provide general guidance, but for specific professional advice, please consult with qualified experts in the relevant field."
    
    def simulate_task_execution(self, task_description):
        """Simulate autonomous task execution"""
        self.task_counter += 1
        
        # Simulate task breakdown
        steps = [
            "🔍 Analyzing task requirements",
            "📊 Gathering relevant information", 
            "🧠 Processing and synthesizing data",
            "📋 Generating structured output"
        ]
        
        result = f"""**Task Execution Simulation**

Task: {task_description}

**Process:**
{chr(10).join(steps)}

**Simulated Analysis:**
Based on the task '{task_description}', I would approach this by:

1. **Research Phase**: Gathering relevant data and context
2. **Analysis Phase**: Processing information systematically  
3. **Synthesis Phase**: Creating actionable insights
4. **Output Phase**: Delivering structured results

**Note**: This is a simulation. For actual implementation, specific tools and real data would be required.

Task ID: lightweight_task_{self.task_counter}
Status: Completed (Simulated)
"""
        return result
    
    def chat(self, message):
        """Main chat interface"""
        intent = self.analyze_intent(message)
        response = self.generate_response(message, intent)
        
        # Store in lightweight conversation history (limit to 10 entries)
        self.conversation_history.append({
            'timestamp': time.time(),
            'message': message,
            'intent': intent,
            'response': response[:200] + "..." if len(response) > 200 else response
        })
        
        # Keep only last 10 conversations to save memory
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
            
        return response
    
    def get_status(self):
        """Get agent status"""
        return {
            'agent_info': {
                'type': 'lightweight_pattern_matcher',
                'version': '1.0.0',
                'memory_optimized': True,
                'uptime_seconds': int(time.time() - self.start_time),
                'conversation_entries': len(self.conversation_history)
            },
            'capabilities': {
                'pattern_matching': True,
                'intent_recognition': True,
                'task_simulation': True,
                'domain_knowledge': True,
                'memory_efficient': True
            },
            'resource_usage': {
                'memory_footprint': 'Very Low (~50MB)',
                'cpu_usage': 'Minimal',
                'suitable_for': 'Free hosting tiers'
            }
        }

# Global agent instance
agent = LightweightAIAgent()

@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'agent_type': 'lightweight_pattern_matcher',
        'memory_optimized': True,
        'timestamp': time.time(),
        'uptime': int(time.time() - agent.start_time)
    })

@app.route('/status', methods=['GET'])
def status():
    """Get detailed status"""
    return jsonify(agent.get_status())

@app.route('/chat', methods=['POST'])
def chat():
    """Chat endpoint"""
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Message required'}), 400
    
    try:
        response = agent.chat(data['message'])
        return jsonify({
            'response': response,
            'text': response,  # Alternative field name for compatibility
            'agent_type': 'Lightweight AI Assistant',
            'timestamp': time.time(),
            'source': 'pattern_matching'
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
            'task_id': f'lightweight_task_{agent.task_counter}',
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
        'message': 'Lightweight AI Agent - Render Free Tier Optimized',
        'status': 'Running efficiently with minimal memory usage',
        'memory_footprint': '~50-80MB (fits comfortably in 512MB limit)',
        'endpoints': {
            'GET /health': 'Health check',
            'GET /status': 'Detailed status',
            'POST /chat': 'Chat interface',
            'POST /execute-task': 'Task execution'
        },
        'optimization': 'Designed for free hosting platforms'
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("🚀 Starting Lightweight AI Agent")
    print(f"📊 Memory optimized for Render free tier (512MB limit)")
    print(f"🌐 Running on port {port}")
    
    app.run(host='0.0.0.0', port=port, debug=False)