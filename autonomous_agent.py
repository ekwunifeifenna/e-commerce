"""
Free Autonomous AI Agent - Render Deployment Ready

Uses local Hugging Face models for completely free AI capabilities
Enhanced for cloud deployment with web interface and general Q&A
"""

import os
import logging
import json
import re
import time
from typing import Dict, Any, List
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app for web deployment
app = Flask(__name__)
CORS(app)

class GeneralKnowledge:
    """Knowledge base for general questions"""
    
    @staticmethod
    def get_current_info() -> Dict[str, str]:
        """Get current system information"""
        return {
            "date": "June 29, 2025",
            "system": "Free AI Agent running on Hugging Face Transformers",
            "capabilities": "File operations, general conversation, code assistance"
        }
    
    @staticmethod
    def programming_help(query: str) -> str:
        """Provide programming assistance"""
        programming_topics = {
            "python": "Python is a versatile programming language great for AI, web development, and automation.",
            "javascript": "JavaScript is essential for web development, both frontend and backend (Node.js).",
            "html": "HTML structures web content. Always use semantic elements for accessibility.",
            "css": "CSS styles web pages. Use flexbox and grid for modern layouts.",
            "react": "React is a popular JavaScript library for building user interfaces with components.",
            "flask": "Flask is a lightweight Python web framework perfect for APIs and small applications.",
            "git": "Git is version control. Key commands: git add, git commit, git push, git pull.",
            "api": "APIs enable communication between applications. REST APIs use HTTP methods.",
            "database": "Databases store data. SQL for relational, NoSQL for flexible data structures."
        }
        
        query_lower = query.lower()
        for topic, info in programming_topics.items():
            if topic in query_lower:
                return f"💡 Programming Help - {topic.title()}: {info}"
        
        return "💡 I can help with Python, JavaScript, HTML, CSS, React, Flask, Git, APIs, and databases. What specific topic interests you?"
    
    @staticmethod
    def general_facts(query: str) -> str:
        """Provide general knowledge"""
        knowledge_base = {
            "ai": "AI (Artificial Intelligence) mimics human intelligence. Machine learning is a subset that learns from data.",
            "internet": "The internet is a global network connecting billions of devices, enabling communication and information sharing.",
            "space": "Space exploration has led to satellites, space stations, and plans for Mars missions.",
            "science": "Science uses observation and experimentation to understand the natural world.",
            "technology": "Technology evolves rapidly, with trends in AI, quantum computing, and renewable energy.",
            "health": "Good health includes proper nutrition, exercise, sleep, and mental wellness practices.",
            "environment": "Environmental protection involves renewable energy, recycling, and sustainable practices.",
            "history": "History helps us understand past events and their impact on the present.",
            "mathematics": "Mathematics is the foundation of science, technology, and logical reasoning.",
            "art": "Art expresses creativity through various mediums like painting, music, literature, and digital media."
        }
        
        query_lower = query.lower()
        for topic, info in knowledge_base.items():
            if topic in query_lower:
                return f"🧠 Knowledge: {info}"
        
        return "🧠 I can discuss AI, technology, science, health, environment, history, mathematics, and art. What interests you?"

class FileOperations:
    """File operation tools for the agent"""
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """Read content from a file"""
        try:
            if file_path.startswith('/') or '..' in file_path:
                return "Error: Access to system files not allowed"
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return f"📄 File content:\n{content}"
        except Exception as e:
            return f"❌ Error reading file: {str(e)}"
    
    @staticmethod
    def write_file(file_path: str, content: str) -> str:
        """Write content to a file"""
        try:
            if file_path.startswith('/') or '..' in file_path:
                return "Error: Access to system files not allowed"
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return f"✅ Successfully wrote to {file_path}"
        except Exception as e:
            return f"❌ Error writing file: {str(e)}"
    
    @staticmethod
    def list_directory(path: str = ".") -> str:
        """List contents of a directory"""
        try:
            if path.startswith('/') or '..' in path:
                return "Error: Access to system directories not allowed"
            
            items = os.listdir(path)
            if not items:
                return "📁 Directory is empty"
            return f"📁 Directory contents: {', '.join(items)}"
        except Exception as e:
            return f"❌ Error listing directory: {str(e)}"

class EnhancedLocalAIAgent:
    """Enhanced Free AI Agent with general knowledge capabilities"""
    
    def __init__(self, model_name="distilgpt2"):
        """Initialize with deployment-optimized model"""
        self.model_name = model_name
        self.model_loaded = False
        
        # Initialize tools and knowledge
        self.file_ops = FileOperations()
        self.knowledge = GeneralKnowledge()
        
        # Available tools
        self.available_tools = {
            "read_file": {
                "function": self.file_ops.read_file,
                "description": "Read content from a file",
                "pattern": r"read_file\(['\"]([^'\"]+)['\"]\)"
            },
            "write_file": {
                "function": self.file_ops.write_file,
                "description": "Write content to a file",
                "pattern": r"write_file\(['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]*)['\"]"
            },
            "list_directory": {
                "function": self.file_ops.list_directory,
                "description": "List directory contents",
                "pattern": r"list_directory\(\)"
            }
        }
        
        # Conversation memory
        self.conversation_history = []
        self.max_history = 3  # Reduced for deployment efficiency
        
        # Try to load model
        self._load_model()
    
    def _load_model(self):
        """Load AI model with fallback options"""
        try:
            logger.info(f"Loading AI model: {self.model_name}")
            
            # Use CPU-only configuration for deployment
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir="./model_cache"
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                cache_dir="./model_cache",
                torch_dtype=torch.float32,  # CPU compatible
                device_map=None  # Force CPU
            )
            
            # Add padding token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Create pipeline
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_length=256,  # Reduced for deployment
                temperature=0.8,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                device=-1  # Force CPU
            )
            
            self.model_loaded = True
            logger.info("✅ AI model loaded successfully")
            
        except Exception as e:
            logger.error(f"❌ Model loading failed: {e}")
            self.model_loaded = False
    
    def _is_general_question(self, query: str) -> bool:
        """Check if query is a general question vs file operation"""
        file_keywords = ["file", "read", "write", "create", "save", "directory", "folder", "list"]
        query_lower = query.lower()
        
        # If no file keywords and doesn't mention specific files
        has_file_keywords = any(keyword in query_lower for keyword in file_keywords)
        has_file_extension = bool(re.search(r'\.\w{2,4}', query))
        
        return not (has_file_keywords or has_file_extension)
    
    def _answer_general_question(self, query: str) -> str:
        """Answer general questions without using AI model"""
        query_lower = query.lower()
        
        # Check for programming questions
        programming_keywords = ["python", "javascript", "html", "css", "react", "flask", "git", "api", "database", "code", "programming", "software"]
        if any(keyword in query_lower for keyword in programming_keywords):
            return self.knowledge.programming_help(query)
        
        # Check for general knowledge
        knowledge_keywords = ["what is", "tell me about", "explain", "how does", "science", "technology", "ai", "space", "health"]
        if any(keyword in query_lower for keyword in knowledge_keywords):
            return self.knowledge.general_facts(query)
        
        # Time/date questions
        if any(word in query_lower for word in ["time", "date", "today", "current"]):
            info = self.knowledge.get_current_info()
            return f"📅 Current date: {info['date']}\n🤖 System: {info['system']}\n⚡ Capabilities: {info['capabilities']}"
        
        # Greeting responses
        greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
        if any(greeting in query_lower for greeting in greetings):
            return "👋 Hello! I'm your free AI assistant. I can help with file operations, programming questions, and general knowledge. What would you like to know?"
        
        # Default response for complex questions
        if self.model_loaded:
            return self._use_ai_model(query)
        else:
            return "🤖 I'm a free AI assistant ready to help! I can assist with:\n📁 File operations (read, write, list)\n💻 Programming questions\n🧠 General knowledge\n\nWhat would you like to know?"
    
    def _use_ai_model(self, query: str) -> str:
        """Use AI model for complex responses"""
        try:
            prompt = f"""You are a helpful AI assistant. Answer the following question clearly and concisely:

Question: {query}
Answer:"""
            
            response = self.generator(
                prompt,
                max_new_tokens=100,
                temperature=0.8,
                do_sample=True
            )[0]['generated_text']
            
            # Extract answer
            answer = response[len(prompt):].strip()
            return answer if answer else "I'll do my best to help with that question!"
            
        except Exception as e:
            logger.error(f"AI model error: {e}")
            return "I'm processing your question. Let me help you with that!"
    
    def _parse_and_execute_tools(self, query: str) -> str:
        """Parse query for tool usage and execute"""
        for tool_name, tool_info in self.available_tools.items():
            match = re.search(tool_info["pattern"], query, re.IGNORECASE)
            if match:
                try:
                    if tool_name == "read_file":
                        return tool_info["function"](match.group(1))
                    elif tool_name == "write_file":
                        return tool_info["function"](match.group(1), match.group(2) if len(match.groups()) > 1 else "")
                    elif tool_name == "list_directory":
                        return tool_info["function"]()
                except Exception as e:
                    return f"❌ Error using {tool_name}: {str(e)}"
        
        # Try natural language file operations
        if "create" in query.lower() and ("file" in query.lower() or ".txt" in query.lower()):
            # Extract filename and content
            filename_match = re.search(r"(?:file|called)\s+['\"]?([^\s'\"]+)['\"]?", query, re.IGNORECASE)
            content_match = re.search(r"(?:with|content)\s+['\"]([^'\"]*)['\"]", query, re.IGNORECASE)
            
            if filename_match:
                filename = filename_match.group(1)
                content = content_match.group(1) if content_match else "Hello from Free AI Agent!"
                return self.file_ops.write_file(filename, content)
        
        return None
    
    def execute_task(self, task: str) -> Dict[str, Any]:
        """Execute task with enhanced capabilities"""
        try:
            start_time = time.time()
            
            # First try tool operations
            tool_result = self._parse_and_execute_tools(task)
            if tool_result:
                execution_time = time.time() - start_time
                return {
                    "status": "completed",
                    "result": tool_result,
                    "type": "tool_operation",
                    "execution_time": round(execution_time, 2)
                }
            
            # Handle general questions
            if self._is_general_question(task):
                result = self._answer_general_question(task)
            else:
                # Suggest file operations
                result = "🤖 I can help with file operations! Try:\n• 'Create a file called example.txt with Hello World'\n• 'Read the file example.txt'\n• 'List directory contents'\n\nOr ask me general questions about programming, science, or technology!"
            
            # Update conversation history
            self.conversation_history.append({
                "human": task,
                "assistant": result
            })
            
            if len(self.conversation_history) > self.max_history:
                self.conversation_history = self.conversation_history[-self.max_history:]
            
            execution_time = time.time() - start_time
            return {
                "status": "completed",
                "result": result,
                "type": "general_response",
                "execution_time": round(execution_time, 2),
                "model_loaded": self.model_loaded
            }
            
        except Exception as e:
            logger.error(f"Task execution error: {str(e)}")
            return {"status": "failed", "error": str(e)}

# Global agent instance
agent = None

def get_agent():
    """Get or create agent instance"""
    global agent
    if agent is None:
        agent = EnhancedLocalAIAgent()
    return agent

# Web Interface HTML
WEB_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <title>Free AI Agent</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 20px; border-radius: 10px; }
        .header { text-align: center; color: #333; margin-bottom: 20px; }
        .chat-box { border: 1px solid #ddd; height: 400px; overflow-y: auto; padding: 10px; margin-bottom: 20px; background: #fafafa; }
        .input-area { display: flex; gap: 10px; }
        input[type="text"] { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background: #e3f2fd; text-align: right; }
        .agent { background: #f1f8e9; }
        .examples { margin: 20px 0; }
        .example { display: inline-block; margin: 5px; padding: 5px 10px; background: #e0e0e0; border-radius: 15px; cursor: pointer; font-size: 12px; }
        .example:hover { background: #d0d0d0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Free AI Agent</h1>
            <p>No API keys required! Powered by Hugging Face Transformers</p>
        </div>
        
        <div class="examples">
            <strong>Try these examples:</strong><br>
            <span class="example" onclick="sendExample('Create a file called hello.txt with Hello World!')">Create file</span>
            <span class="example" onclick="sendExample('List directory contents')">List files</span>
            <span class="example" onclick="sendExample('What is artificial intelligence?')">Ask about AI</span>
            <span class="example" onclick="sendExample('Help me with Python programming')">Programming help</span>
            <span class="example" onclick="sendExample('Tell me about space exploration')">General knowledge</span>
        </div>
        
        <div class="chat-box" id="chatBox"></div>
        
        <div class="input-area">
            <input type="text" id="userInput" placeholder="Ask me anything or request file operations..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        function addMessage(content, isUser) {
            const chatBox = document.getElementById('chatBox');
            const message = document.createElement('div');
            message.className = `message ${isUser ? 'user' : 'agent'}`;
            message.innerHTML = content.replace(/\\n/g, '<br>');
            chatBox.appendChild(message);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function sendExample(text) {
            document.getElementById('userInput').value = text;
            sendMessage();
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') {
                sendMessage();
            }
        }

        async function sendMessage() {
            const input = document.getElementById('userInput');
            const message = input.value.trim();
            if (!message) return;

            addMessage(message, true);
            input.value = '';

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                addMessage(data.result || data.error || 'No response', false);
            } catch (error) {
                addMessage('Error: ' + error.message, false);
            }
        }

        // Initial welcome message
        addMessage('👋 Welcome! I\\'m your free AI assistant. I can help with file operations, programming questions, and general knowledge. What would you like to know?', false);
    </script>
</body>
</html>
"""

# Flask Routes
@app.route('/')
def home():
    """Serve web interface"""
    return render_template_string(WEB_INTERFACE)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({"error": "No message provided"})
        
        # Get agent and process message
        current_agent = get_agent()
        result = current_agent.execute_task(message)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"error": str(e)})

@app.route('/health')
def health():
    """Health check for deployment"""
    current_agent = get_agent()
    return jsonify({
        "status": "healthy",
        "model_loaded": current_agent.model_loaded if current_agent else False,
        "timestamp": time.time()
    })

def main():
    """Main function for both local and deployment"""
    port = int(os.environ.get('PORT', 5000))
    
    if os.environ.get('PORT'):
        # Cloud deployment mode
        print("🌐 Starting Free AI Agent for deployment...")
        app.run(host='0.0.0.0', port=port)
    else:
        # Local development mode
        print("🤖 Free AI Agent - Local Development Mode")
        print(f"🌐 Web interface available at: http://localhost:{port}")
        print("💻 Starting interactive mode as well...")
        
        # Start web server in background and interactive mode
        import threading
        
        def run_web():
            app.run(host='localhost', port=port, debug=False)
        
        web_thread = threading.Thread(target=run_web, daemon=True)
        web_thread.start()
        
        # Interactive CLI mode
        agent = get_agent()
        print("\n💬 Interactive chat mode (type 'exit' to quit, 'web' for web interface):")
        
        while True:
            user_input = input("\n🙋 You: ").strip()
            if user_input.lower() == 'exit':
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'web':
                print(f"🌐 Open http://localhost:{port} in your browser")
                continue
                
            if user_input:
                result = agent.execute_task(user_input)
                print(f"🤖 AI: {result.get('result', result.get('error'))}")

if __name__ == "__main__":
    main()