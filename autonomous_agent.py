"""
Free Autonomous AI Agent - Render Deployment Ready

Lightweight version optimized for cloud deployment
No heavy AI models - uses built-in knowledge base for responses
"""

import os
import logging
import json
import re
import time
from typing import Dict, Any, List
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app for web deployment
app = Flask(__name__)
CORS(app)

class GeneralKnowledge:
    """Enhanced knowledge base for general questions"""
    
    @staticmethod
    def get_current_info() -> Dict[str, str]:
        """Get current system information"""
        return {
            "date": "June 29, 2025",
            "system": "Free AI Agent - Lightweight Cloud Version",
            "capabilities": "File operations, general conversation, programming help, knowledge base"
        }
    
    @staticmethod
    def programming_help(query: str) -> str:
        """Provide detailed programming assistance"""
        programming_topics = {
            "python": "Python is a versatile programming language. Key concepts: variables, functions, classes, modules. Popular frameworks: Django, Flask, FastAPI. Use pip for package management.",
            "javascript": "JavaScript powers web development. ES6+ features: arrow functions, async/await, destructuring. Frameworks: React, Vue, Angular. Node.js for backend.",
            "html": "HTML structures web content. Semantic elements: header, nav, main, section, article, footer. Always include DOCTYPE, lang attribute, and meta viewport.",
            "css": "CSS styles web pages. Modern layouts: Flexbox (display: flex), Grid (display: grid). Responsive design with media queries. CSS custom properties (variables).",
            "react": "React builds UIs with components. Key concepts: JSX, props, state, hooks (useState, useEffect). Create components as functions, manage state with hooks.",
            "flask": "Flask is a Python web framework. Basic app: from flask import Flask; app = Flask(__name__). Routes with @app.route('/path'). Templates with render_template.",
            "git": "Git version control commands: git init, git add ., git commit -m 'message', git push, git pull, git branch, git merge, git status.",
            "api": "APIs connect applications. REST uses HTTP methods: GET (read), POST (create), PUT (update), DELETE (remove). JSON for data exchange.",
            "database": "SQL databases: PostgreSQL, MySQL. NoSQL: MongoDB, Redis. ORM libraries: SQLAlchemy (Python), Prisma (JS). Always sanitize queries.",
            "docker": "Docker containerizes applications. Dockerfile defines image. docker build, docker run, docker-compose for multi-container apps.",
            "deployment": "Deploy to cloud: Heroku, Render, Vercel, Netlify. Use environment variables for secrets. CI/CD with GitHub Actions."
        }
        
        query_lower = query.lower()
        for topic, info in programming_topics.items():
            if topic in query_lower:
                return f"💡 Programming Help - {topic.title()}:\n{info}\n\n🔧 Need specific code examples? Ask for '{topic} example'!"
        
        # Code examples
        if "example" in query_lower:
            examples = {
                "python": """
# Python Example - Web Scraper
import requests
from bs4 import BeautifulSoup

def scrape_title(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.find('title').text

print(scrape_title('https://example.com'))
""",
                "javascript": """
// JavaScript Example - Async API Call
async function fetchUserData(userId) {
    try {
        const response = await fetch(`/api/users/${userId}`);
        const user = await response.json();
        return user;
    } catch (error) {
        console.error('Error:', error);
    }
}

fetchUserData(123).then(user => console.log(user));
""",
                "react": """
// React Example - Todo Component
import React, { useState } from 'react';

function TodoApp() {
    const [todos, setTodos] = useState([]);
    const [input, setInput] = useState('');
    
    const addTodo = () => {
        setTodos([...todos, { id: Date.now(), text: input }]);
        setInput('');
    };
    
    return (
        <div>
            <input value={input} onChange={(e) => setInput(e.target.value)} />
            <button onClick={addTodo}>Add Todo</button>
            {todos.map(todo => <div key={todo.id}>{todo.text}</div>)}
        </div>
    );
}
""",
                "flask": """
# Flask Example - REST API
from flask import Flask, jsonify, request

app = Flask(__name__)
users = []

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def create_user():
    user = request.json
    users.append(user)
    return jsonify(user), 201

if __name__ == '__main__':
    app.run(debug=True)
"""
            }
            
            for lang, code in examples.items():
                if lang in query_lower:
                    return f"💻 {lang.title()} Code Example:\n```{lang}\n{code}\n```"
        
        return "💡 I can help with Python, JavaScript, HTML, CSS, React, Flask, Git, APIs, databases, Docker, and deployment. Ask for specific topics or code examples!"
    
    @staticmethod
    def general_facts(query: str) -> str:
        """Provide comprehensive general knowledge"""
        knowledge_base = {
            "ai": """Artificial Intelligence (AI) simulates human intelligence in machines. Types:
• Machine Learning: Learns from data (supervised, unsupervised, reinforcement)
• Deep Learning: Neural networks with multiple layers
• Natural Language Processing: Understanding and generating human language
• Computer Vision: Analyzing and understanding images/video
Popular frameworks: TensorFlow, PyTorch, scikit-learn""",
            
            "internet": """The Internet is a global network connecting billions of devices worldwide:
• Created in the 1960s-70s (ARPANET), public since 1990s
• Uses TCP/IP protocol suite for communication
• World Wide Web (WWW) runs on top of the internet
• Key technologies: HTTP/HTTPS, DNS, routers, ISPs
• Modern trends: Cloud computing, IoT, 5G networks""",
            
            "space": """Space exploration achievements and future:
• 1957: Sputnik (first satellite)
• 1969: Moon landing (Apollo 11)
• Current: International Space Station, Mars rovers
• Private companies: SpaceX, Blue Origin, Virgin Galactic
• Future goals: Mars colonization, asteroid mining, space tourism""",
            
            "technology": """Current technology trends shaping the future:
• Artificial Intelligence and Machine Learning
• Cloud Computing and Edge Computing
• Internet of Things (IoT) and Smart Cities
• Blockchain and Cryptocurrency
• Quantum Computing research
• Renewable Energy and Electric Vehicles
• Augmented/Virtual Reality (AR/VR)""",
            
            "science": """Scientific method drives human understanding:
• Observation → Hypothesis → Experiment → Analysis → Conclusion
• Major fields: Physics, Chemistry, Biology, Earth Sciences
• Recent breakthroughs: CRISPR gene editing, gravitational waves
• Climate science: Understanding global warming and solutions
• Medical advances: mRNA vaccines, personalized medicine""",
            
            "health": """Comprehensive health and wellness:
• Physical: Regular exercise, balanced nutrition, adequate sleep
• Mental: Stress management, mindfulness, social connections
• Preventive care: Regular check-ups, vaccinations
• Modern challenges: Sedentary lifestyle, processed foods
• Digital health: Wearables, telemedicine, health apps"""
        }
        
        query_lower = query.lower()
        for topic, info in knowledge_base.items():
            if topic in query_lower:
                return f"🧠 Knowledge - {topic.title()}:\n{info}"
        
        # Handle specific questions
        if "how" in query_lower:
            return "🤔 I'd be happy to explain how something works! Could you be more specific about what you'd like to understand?"
        
        return "🧠 I can discuss AI, technology, science, space, internet, health, and many other topics. What specific subject interests you?"

class SmartResponder:
    """Advanced response system without heavy AI models"""
    
    @staticmethod
    def generate_response(query: str, context: List[Dict] = None) -> str:
        """Generate contextual responses using pattern matching and templates"""
        query_lower = query.lower()
        
        # Question types
        question_words = ["what", "how", "why", "when", "where", "who"]
        is_question = any(word in query_lower for word in question_words) or query.endswith("?")
        
        # Sentiment analysis (simple)
        positive_words = ["good", "great", "awesome", "excellent", "love", "like", "happy"]
        negative_words = ["bad", "terrible", "hate", "dislike", "sad", "angry", "frustrated"]
        
        has_positive = any(word in query_lower for word in positive_words)
        has_negative = any(word in query_lower for word in negative_words)
        
        # Context-aware responses
        if "thank" in query_lower:
            return "You're welcome! I'm here to help whenever you need assistance. 😊"
        
        if any(word in query_lower for word in ["help", "assist", "support"]):
            return """🤖 I'm here to help! I can assist with:

📁 **File Operations**: Create, read, write files and list directories
💻 **Programming**: Python, JavaScript, React, Flask, Git, APIs, databases
🧠 **General Knowledge**: Science, technology, AI, space, health
💡 **Problem Solving**: Debug code, explain concepts, provide examples

What would you like help with today?"""
        
        if is_question and "you" in query_lower:
            return """🤖 About me: I'm a free AI assistant that runs entirely on open-source technology. I can:
• Help with programming and coding questions
• Perform file operations safely
• Share knowledge on various topics
• Provide code examples and explanations

I don't require API keys or expensive cloud services - I'm designed to be accessible and helpful!"""
        
        # Default intelligent response
        if is_question:
            return "🤔 That's an interesting question! I'd be happy to help you explore that topic. Could you provide a bit more context or specify what aspect you're most curious about?"
        
        return "💭 I understand you're sharing something with me. Feel free to ask questions or let me know how I can help!"

class FileOperations:
    """Enhanced file operation tools"""
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """Read content from a file with safety checks"""
        try:
            # Security: Prevent access to system files
            if file_path.startswith('/') or '..' in file_path or file_path.startswith('~'):
                return "🚫 Error: Access to system files not allowed for security"
            
            # Check file size to prevent memory issues
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                if file_size > 1024 * 1024:  # 1MB limit
                    return f"📄 File is large ({file_size} bytes). Showing first 1000 characters:\n{open(file_path, 'r').read(1000)}..."
            
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            return f"📄 **{file_path}** ({len(content)} characters):\n```\n{content}\n```"
            
        except FileNotFoundError:
            return f"❌ File '{file_path}' not found. Use 'list_directory()' to see available files."
        except PermissionError:
            return f"🚫 Permission denied accessing '{file_path}'"
        except Exception as e:
            return f"❌ Error reading file: {str(e)}"
    
    @staticmethod
    def write_file(file_path: str, content: str) -> str:
        """Write content to a file with validation"""
        try:
            # Security checks
            if file_path.startswith('/') or '..' in file_path or file_path.startswith('~'):
                return "🚫 Error: Access to system paths not allowed for security"
            
            # Validate content length
            if len(content) > 10 * 1024 * 1024:  # 10MB limit
                return "❌ Content too large (max 10MB allowed)"
            
            # Create directory if needed
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            return f"✅ Successfully created '{file_path}' ({len(content)} characters)\n💡 Use read_file('{file_path}') to view the content"
            
        except Exception as e:
            return f"❌ Error writing file: {str(e)}"
    
    @staticmethod
    def list_directory(path: str = ".") -> str:
        """List directory contents with detailed information"""
        try:
            # Security check
            if path.startswith('/') or '..' in path:
                return "🚫 Error: Access to system directories not allowed"
            
            if not os.path.exists(path):
                return f"❌ Directory '{path}' does not exist"
            
            items = []
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    items.append(f"📁 {item}/")
                else:
                    size = os.path.getsize(item_path)
                    items.append(f"📄 {item} ({size} bytes)")
            
            if not items:
                return f"📁 Directory '{path}' is empty"
            
            return f"📁 **Directory: {path}**\n" + "\n".join(sorted(items))
            
        except Exception as e:
            return f"❌ Error listing directory: {str(e)}"

class LightweightAIAgent:
    """Lightweight AI Agent optimized for cloud deployment"""
    
    def __init__(self):
        """Initialize agent with knowledge base only"""
        self.file_ops = FileOperations()
        self.knowledge = GeneralKnowledge()
        self.responder = SmartResponder()
        
        # Available tools with patterns
        self.available_tools = {
            "read_file": {
                "function": self.file_ops.read_file,
                "description": "Read content from a file",
                "patterns": [
                    r"read_file\(['\"]([^'\"]+)['\"]\)",
                    r"read\s+(?:the\s+)?file\s+['\"]?([^\s'\"]+)['\"]?",
                    r"show\s+(?:me\s+)?(?:the\s+)?(?:contents?\s+of\s+)?['\"]?([^\s'\"]+)['\"]?"
                ]
            },
            "write_file": {
                "function": self.file_ops.write_file,
                "description": "Write content to a file",
                "patterns": [
                    r"write_file\(['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]*)['\"]",
                    r"create\s+(?:a\s+)?file\s+(?:called\s+|named\s+)?['\"]?([^\s'\"]+)['\"]?(?:\s+with\s+['\"]([^'\"]*)['\"])?",
                    r"save\s+['\"]([^'\"]*)['\"]?\s+(?:to\s+|as\s+)['\"]?([^\s'\"]+)['\"]?"
                ]
            },
            "list_directory": {
                "function": self.file_ops.list_directory,
                "description": "List directory contents",
                "patterns": [
                    r"list_directory\(\)",
                    r"list\s+(?:the\s+)?(?:directory|folder|files)",
                    r"show\s+(?:me\s+)?(?:the\s+)?(?:directory|folder|files)",
                    r"what\s+(?:files|items)\s+(?:are\s+)?(?:here|available)"
                ]
            }
        }
        
        # Conversation memory for context
        self.conversation_history = []
        self.max_history = 5
        
        logger.info("✅ Lightweight AI Agent initialized successfully")
    
    def _parse_and_execute_tools(self, query: str) -> str:
        """Parse and execute tool operations with multiple patterns"""
        query = query.strip()
        
        for tool_name, tool_info in self.available_tools.items():
            for pattern in tool_info["patterns"]:
                match = re.search(pattern, query, re.IGNORECASE)
                if match:
                    try:
                        if tool_name == "read_file":
                            return tool_info["function"](match.group(1))
                        elif tool_name == "write_file":
                            filename = match.group(1) if match.group(1) else match.group(2)
                            content = match.group(2) if len(match.groups()) > 1 and match.group(2) else "Hello from Free AI Agent!"
                            # Handle reversed order for some patterns
                            if "save" in pattern:
                                content, filename = filename, content
                            return tool_info["function"](filename, content)
                        elif tool_name == "list_directory":
                            return tool_info["function"]()
                    except Exception as e:
                        return f"❌ Error using {tool_name}: {str(e)}"
        
        return None
    
    def _get_response_type(self, query: str) -> str:
        """Determine the type of response needed"""
        query_lower = query.lower()
        
        # File operations
        file_keywords = ["file", "read", "write", "create", "save", "directory", "folder", "list"]
        if any(keyword in query_lower for keyword in file_keywords):
            return "file_operation"
        
        # Programming questions
        prog_keywords = ["python", "javascript", "html", "css", "react", "flask", "git", "api", "database", "code", "programming"]
        if any(keyword in query_lower for keyword in prog_keywords):
            return "programming_help"
        
        # General knowledge
        knowledge_keywords = ["what is", "tell me about", "explain", "how does", "science", "technology", "ai", "space"]
        if any(keyword in query_lower for keyword in knowledge_keywords):
            return "general_knowledge"
        
        return "general_chat"
    
    def execute_task(self, task: str) -> Dict[str, Any]:
        """Execute task with comprehensive handling"""
        try:
            start_time = time.time()
            
            # First try tool operations
            tool_result = self._parse_and_execute_tools(task)
            if tool_result:
                self._update_conversation_history(task, tool_result)
                return {
                    "status": "completed",
                    "result": tool_result,
                    "type": "tool_operation",
                    "execution_time": round(time.time() - start_time, 2)
                }
            
            # Determine response type and generate appropriate response
            response_type = self._get_response_type(task)
            
            if response_type == "programming_help":
                result = self.knowledge.programming_help(task)
            elif response_type == "general_knowledge":
                result = self.knowledge.general_facts(task)
            elif response_type == "file_operation":
                result = """🔧 **File Operations Available:**
                
• **Create file**: "Create a file called example.txt with Hello World"
• **Read file**: "Read the file example.txt" or "Show me example.txt"
• **List files**: "List directory" or "Show me the files"

Try one of these commands or ask for help with specific file operations!"""
            else:
                result = self.responder.generate_response(task, self.conversation_history)
            
            # Update conversation history
            self._update_conversation_history(task, result)
            
            return {
                "status": "completed",
                "result": result,
                "type": response_type,
                "execution_time": round(time.time() - start_time, 2)
            }
            
        except Exception as e:
            logger.error(f"Task execution error: {str(e)}")
            return {
                "status": "failed", 
                "error": f"I encountered an error: {str(e)}. Please try rephrasing your request.",
                "type": "error"
            }
    
    def _update_conversation_history(self, user_input: str, response: str):
        """Update conversation history for context"""
        self.conversation_history.append({
            "user": user_input,
            "assistant": response,
            "timestamp": time.time()
        })
        
        if len(self.conversation_history) > self.max_history:
            self.conversation_history = self.conversation_history[-self.max_history:]

# Global agent instance
agent = None

def get_agent():
    """Get or create agent instance"""
    global agent
    if agent is None:
        agent = LightweightAIAgent()
    return agent

# Web Interface HTML
WEB_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <title>Free AI Agent - Cloud Ready</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; 
            margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container { 
            max-width: 900px; margin: 0 auto; background: white; 
            border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header { 
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            color: white; padding: 30px; text-align: center; margin: 0;
        }
        .header h1 { margin: 0; font-size: 2.5em; font-weight: 300; }
        .header p { margin: 10px 0 0 0; opacity: 0.9; font-size: 1.1em; }
        .status { 
            background: #27ae60; color: white; padding: 10px; text-align: center; 
            font-weight: bold; font-size: 0.9em;
        }
        .examples { 
            padding: 20px; background: #f8f9fa; border-bottom: 1px solid #e9ecef;
        }
        .examples-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 10px; margin-top: 15px;
        }
        .example { 
            padding: 12px 16px; background: #fff; border: 2px solid #e9ecef;
            border-radius: 25px; cursor: pointer; text-align: center;
            transition: all 0.2s; font-size: 0.9em; font-weight: 500;
        }
        .example:hover { 
            background: #3498db; color: white; border-color: #3498db;
            transform: translateY(-2px); box-shadow: 0 5px 15px rgba(52,152,219,0.3);
        }
        .chat-container { padding: 20px; }
        .chat-box { 
            height: 450px; overflow-y: auto; padding: 20px; margin-bottom: 20px; 
            background: #f8f9fa; border-radius: 10px; border: 1px solid #e9ecef;
        }
        .message { 
            margin: 15px 0; padding: 15px 20px; border-radius: 20px; 
            max-width: 80%; word-wrap: break-word; line-height: 1.5;
        }
        .user { 
            background: linear-gradient(135deg, #3498db, #2980b9); 
            color: white; margin-left: auto; border-bottom-right-radius: 5px;
        }
        .agent { 
            background: white; border: 2px solid #ecf0f1; 
            border-bottom-left-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .input-area { 
            display: flex; gap: 15px; padding: 20px; background: #f8f9fa;
            border-radius: 10px; margin-top: 10px;
        }
        .input-container { flex: 1; position: relative; }
        input[type="text"] { 
            width: 100%; padding: 15px 20px; border: 2px solid #e9ecef; 
            border-radius: 25px; font-size: 16px; outline: none;
            transition: border-color 0.2s;
        }
        input[type="text"]:focus { border-color: #3498db; }
        button { 
            padding: 15px 30px; background: linear-gradient(135deg, #27ae60, #2ecc71);
            color: white; border: none; border-radius: 25px; cursor: pointer; 
            font-size: 16px; font-weight: bold; transition: all 0.2s;
            min-width: 100px;
        }
        button:hover { 
            background: linear-gradient(135deg, #219a52, #27ae60);
            transform: translateY(-2px); box-shadow: 0 5px 15px rgba(39,174,96,0.3);
        }
        .typing { opacity: 0.7; font-style: italic; }
        pre { background: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 8px; overflow-x: auto; }
        code { background: #ecf0f1; padding: 2px 6px; border-radius: 4px; font-family: 'Monaco', 'Consolas', monospace; }
        
        @media (max-width: 768px) {
            body { padding: 10px; }
            .header h1 { font-size: 2em; }
            .examples-grid { grid-template-columns: 1fr; }
            .input-area { flex-direction: column; gap: 10px; }
            .message { max-width: 95%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Free AI Agent</h1>
            <p>Lightweight • No API Keys • Cloud Ready</p>
        </div>
        
        <div class="status">
            ✅ Online & Ready • File Operations • Programming Help • General Knowledge
        </div>
        
        <div class="examples">
            <strong>💡 Try these examples:</strong>
            <div class="examples-grid">
                <div class="example" onclick="sendExample('Create a file called hello.txt with Hello World!')">📄 Create File</div>
                <div class="example" onclick="sendExample('List directory contents')">📁 List Files</div>
                <div class="example" onclick="sendExample('What is artificial intelligence?')">🧠 Ask about AI</div>
                <div class="example" onclick="sendExample('Help me with Python programming')">💻 Python Help</div>
                <div class="example" onclick="sendExample('Show me a React example')">⚛️ React Code</div>
                <div class="example" onclick="sendExample('Explain how APIs work')">🔗 Learn APIs</div>
            </div>
        </div>
        
        <div class="chat-container">
            <div class="chat-box" id="chatBox"></div>
            
            <div class="input-area">
                <div class="input-container">
                    <input type="text" id="userInput" placeholder="Ask me anything - file operations, programming, or general questions..." onkeypress="handleKeyPress(event)">
                </div>
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>

    <script>
        function formatMessage(content) {
            // Convert markdown-like formatting
            content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            content = content.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
            content = content.replace(/`([^`]+)`/g, '<code>$1</code>');
            content = content.replace(/\n/g, '<br>');
            return content;
        }

        function addMessage(content, isUser) {
            const chatBox = document.getElementById('chatBox');
            const message = document.createElement('div');
            message.className = `message ${isUser ? 'user' : 'agent'}`;
            message.innerHTML = isUser ? content : formatMessage(content);
            chatBox.appendChild(message);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function addTypingIndicator() {
            const chatBox = document.getElementById('chatBox');
            const typing = document.createElement('div');
            typing.className = 'message agent typing';
            typing.id = 'typing';
            typing.innerHTML = '🤖 Thinking...';
            chatBox.appendChild(typing);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function removeTypingIndicator() {
            const typing = document.getElementById('typing');
            if (typing) typing.remove();
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
            addTypingIndicator();

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: message })
                });

                const data = await response.json();
                removeTypingIndicator();
                addMessage(data.result || data.error || 'No response received', false);
            } catch (error) {
                removeTypingIndicator();
                addMessage('❌ Connection error: ' + error.message, false);
            }
        }

        // Initial welcome message
        window.onload = function() {
            addMessage(`👋 **Welcome to Free AI Agent!**

I'm your lightweight AI assistant that works entirely in the cloud without requiring any API keys or external services.

**I can help you with:**
• 📁 File operations (create, read, list files)
• 💻 Programming questions and code examples  
• 🧠 General knowledge and explanations
• 🔧 Technical problem solving

Try the examples above or ask me anything!`, false);
        };
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
        return jsonify({"error": f"Server error: {str(e)}"})

@app.route('/health')
def health():
    """Health check for deployment"""
    return jsonify({
        "status": "healthy",
        "version": "lightweight",
        "timestamp": time.time(),
        "memory_optimized": True
    })

# Main function for deployment
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    
    if os.environ.get('PORT'):
        # Cloud deployment mode
        logger.info("🌐 Starting Free AI Agent for cloud deployment...")
        app.run(host='0.0.0.0', port=port)
    else:
        # Local development mode
        logger.info("🤖 Free AI Agent - Local Development Mode")
        logger.info(f"🌐 Web interface: http://localhost:{port}")
        app.run(host='localhost', port=port, debug=True)