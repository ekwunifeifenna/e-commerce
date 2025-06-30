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
    """Advanced response system with enhanced natural language understanding"""
    
    def __init__(self):
        """Initialize with enhanced NLP patterns and intent mapping"""
        # Intent patterns for better query understanding
        self.intent_patterns = {
            'file_operations': {
                'create': [r'create\s+(?:a\s+)?file', r'make\s+(?:a\s+)?file', r'new\s+file', r'write\s+to'],
                'read': [r'read\s+(?:the\s+)?file', r'show\s+(?:me\s+)?(?:the\s+)?content', r'open\s+file', r'display\s+file'],
                'list': [r'list\s+(?:all\s+)?files', r'show\s+(?:me\s+)?(?:all\s+)?files', r'directory\s+content', r'what\s+files'],
                'delete': [r'delete\s+(?:the\s+)?file', r'remove\s+(?:the\s+)?file', r'erase\s+file']
            },
            'programming_help': {
                'explain': [r'explain\s+(?:how\s+)?(?:to\s+)?', r'what\s+is\s+', r'how\s+does\s+.*\s+work', r'tell\s+me\s+about'],
                'code_example': [r'show\s+(?:me\s+)?(?:an?\s+)?example', r'give\s+(?:me\s+)?(?:an?\s+)?example', r'sample\s+code'],
                'debug': [r'debug\s+(?:this\s+)?code', r'fix\s+(?:this\s+)?(?:code|error)', r'what\'?s\s+wrong\s+with'],
                'best_practices': [r'best\s+practices?', r'good\s+practices?', r'recommended\s+way']
            },
            'general_knowledge': {
                'definition': [r'what\s+is\s+(?:an?\s+)?', r'define\s+', r'meaning\s+of'],
                'comparison': [r'difference\s+between', r'compare\s+', r'.*\s+vs\s+.*', r'.*\s+versus\s+.*'],
                'process': [r'how\s+to\s+', r'steps\s+to\s+', r'process\s+of', r'way\s+to\s+'],
                'advantages': [r'benefits?\s+of', r'advantages?\s+of', r'pros?\s+of', r'why\s+use']
            },
            'task_execution': {
                'analysis': [r'analyz[ae]\s+', r'examine\s+', r'investigate\s+', r'study\s+'],
                'research': [r'research\s+', r'find\s+information\s+about', r'look\s+up\s+'],
                'generate': [r'generate\s+', r'create\s+', r'produce\s+', r'make\s+'],
                'optimize': [r'optimize\s+', r'improve\s+', r'enhance\s+', r'better\s+way\s+to']
            }
        }
        
        # Context keywords for better understanding
        self.context_keywords = {
            'urgency': ['urgent', 'asap', 'quickly', 'fast', 'immediately', 'rush'],
            'uncertainty': ['maybe', 'perhaps', 'possibly', 'might', 'could', 'unsure'],
            'certainty': ['definitely', 'certainly', 'absolutely', 'sure', 'confident'],
            'difficulty': ['difficult', 'hard', 'complex', 'challenging', 'complicated'],
            'simplicity': ['simple', 'easy', 'basic', 'straightforward', 'quick']
        }
        
        # Enhanced sentiment analysis
        self.sentiment_words = {
            'positive': ['good', 'great', 'awesome', 'excellent', 'amazing', 'fantastic', 'wonderful', 'perfect', 'love', 'like', 'happy', 'pleased', 'satisfied'],
            'negative': ['bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'angry', 'frustrated', 'disappointed', 'upset', 'annoyed'],
            'neutral': ['okay', 'fine', 'alright', 'decent', 'average', 'normal', 'standard']
        }
    
    def analyze_query_intent(self, query: str) -> dict:
        """Analyze query to determine intent, entities, and context"""
        query_lower = query.lower()
        analysis = {
            'primary_intent': 'general_chat',
            'sub_intent': None,
            'entities': [],
            'context': {
                'is_question': False,
                'sentiment': 'neutral',
                'urgency': 'normal',
                'complexity': 'normal'
            },
            'confidence': 0.0
        }
        
        # Detect if it's a question
        question_indicators = ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'can', 'could', 'would', 'should', 'is', 'are', 'do', 'does', 'did']
        analysis['context']['is_question'] = (
            any(query_lower.startswith(word) for word in question_indicators) or 
            query.endswith('?') or
            ' or ' in query_lower
        )
        
        # Intent detection with confidence scoring
        max_confidence = 0
        for intent_category, sub_intents in self.intent_patterns.items():
            for sub_intent, patterns in sub_intents.items():
                confidence = 0
                for pattern in patterns:
                    if re.search(pattern, query_lower):
                        confidence += 1
                
                if confidence > max_confidence:
                    max_confidence = confidence
                    analysis['primary_intent'] = intent_category
                    analysis['sub_intent'] = sub_intent
                    analysis['confidence'] = min(confidence / len(patterns), 1.0)
        
        # Entity extraction (file names, programming languages, etc.)
        # File names
        file_pattern = r'([a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9]+)'
        files = re.findall(file_pattern, query)
        analysis['entities'].extend([{'type': 'file', 'value': f} for f in files])
        
        # Programming languages
        prog_langs = ['python', 'javascript', 'java', 'c++', 'html', 'css', 'react', 'flask', 'node', 'sql']
        for lang in prog_langs:
            if lang in query_lower:
                analysis['entities'].append({'type': 'programming_language', 'value': lang})
        
        # Context analysis
        for context_type, keywords in self.context_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                if context_type == 'urgency':
                    analysis['context']['urgency'] = 'high'
                elif context_type in ['difficulty', 'simplicity']:
                    analysis['context']['complexity'] = context_type
        
        # Sentiment analysis
        sentiment_scores = {}
        for sentiment, words in self.sentiment_words.items():
            score = sum(1 for word in words if word in query_lower)
            if score > 0:
                sentiment_scores[sentiment] = score
        
        if sentiment_scores:
            analysis['context']['sentiment'] = max(sentiment_scores, key=sentiment_scores.get)
        
        return analysis
    
    def generate_contextual_response(self, query: str, analysis: dict, context: List[Dict] = None) -> str:
        """Generate response based on detailed query analysis"""
        intent = analysis['primary_intent']
        sub_intent = analysis['sub_intent']
        entities = analysis['entities']
        query_context = analysis['context']
        
        # Handle different intents with context awareness
        if intent == 'file_operations':
            return self._handle_file_operations_intent(query, sub_intent, entities, query_context)
        elif intent == 'programming_help':
            return self._handle_programming_intent(query, sub_intent, entities, query_context)
        elif intent == 'general_knowledge':
            return self._handle_knowledge_intent(query, sub_intent, entities, query_context)
        elif intent == 'task_execution':
            return self._handle_task_intent(query, sub_intent, entities, query_context)
        else:
            return self._handle_general_chat(query, query_context, context)
    
    def _handle_file_operations_intent(self, query: str, sub_intent: str, entities: list, context: dict) -> str:
        """Handle file operation intents with context"""
        urgency_modifier = " I'll help you with that right away!" if context['urgency'] == 'high' else ""
        
        if sub_intent == 'create':
            files = [e['value'] for e in entities if e['type'] == 'file']
            if files:
                return f"📄 I'll help you create the file '{files[0]}'.{urgency_modifier} Use the format: create file called {files[0]} with [your content]"
            return f"📄 I can help you create a file.{urgency_modifier} What would you like to name it and what content should it contain?"
        
        elif sub_intent == 'read':
            files = [e['value'] for e in entities if e['type'] == 'file']
            if files:
                return f"📖 I'll read the file '{files[0]}' for you.{urgency_modifier} Let me fetch its contents."
            return f"📖 I can read a file for you.{urgency_modifier} Which file would you like me to read?"
        
        elif sub_intent == 'list':
            return f"📁 I'll show you all the files in the directory.{urgency_modifier} Here's what's available:"
        
        return "🔧 I can help with file operations like creating, reading, or listing files. What specific operation would you like to perform?"
    
    def _handle_programming_intent(self, query: str, sub_intent: str, entities: list, context: dict) -> str:
        """Handle programming help intents"""
        languages = [e['value'] for e in entities if e['type'] == 'programming_language']
        complexity_note = ""
        
        if context['complexity'] == 'difficulty':
            complexity_note = " I'll break this down into simple steps to make it easier to understand."
        elif context['complexity'] == 'simplicity':
            complexity_note = " I'll keep this concise and straightforward."
        
        if sub_intent == 'explain' and languages:
            return f"💡 I'll explain {languages[0]} concepts for you.{complexity_note} What specific aspect would you like me to cover?"
        
        elif sub_intent == 'code_example' and languages:
            return f"💻 I'll provide a {languages[0]} code example.{complexity_note} What functionality are you looking to implement?"
        
        elif sub_intent == 'debug':
            return f"🐛 I'll help you debug your code.{complexity_note} Please share the code and describe the issue you're experiencing."
        
        elif sub_intent == 'best_practices' and languages:
            return f"⭐ I'll share {languages[0]} best practices with you.{complexity_note} Are you interested in general practices or something specific?"
        
        return f"💻 I can help with programming questions.{complexity_note} What programming topic or language would you like assistance with?"
    
    def _handle_knowledge_intent(self, query: str, sub_intent: str, entities: list, context: dict) -> str:
        """Handle general knowledge intents"""
        if sub_intent == 'definition':
            return "🧠 I'll explain that concept for you. What specifically would you like me to define?"
        elif sub_intent == 'comparison':
            return "⚖️ I can help compare different concepts or technologies. What would you like me to compare?"
        elif sub_intent == 'process':
            return "📋 I'll walk you through the process step by step. What process are you interested in learning about?"
        elif sub_intent == 'advantages':
            return "✅ I'll explain the benefits and advantages. What topic are you evaluating?"
        
        return "🧠 I can share knowledge on various topics including technology, science, and general concepts. What would you like to learn about?"
    
    def _handle_task_intent(self, query: str, sub_intent: str, entities: list, context: dict) -> str:
        """Handle task execution intents"""
        if sub_intent == 'analysis':
            return "🔍 I'll analyze that for you. What specific data or topic would you like me to examine?"
        elif sub_intent == 'research':
            return "🔬 I can help research that topic. What specific information are you looking for?"
        elif sub_intent == 'generate':
            return "⚡ I'll generate that for you. What type of content or code would you like me to create?"
        elif sub_intent == 'optimize':
            return "🚀 I'll help optimize that. What specifically would you like to improve?"
        
        return "🎯 I can help execute various tasks. What would you like me to work on?"
    
    def _handle_general_chat(self, query: str, context: dict, conversation_history: list) -> str:
        """Handle general conversation with context awareness"""
        query_lower = query.lower()
        
        # Gratitude responses
        if any(word in query_lower for word in ['thank', 'thanks', 'appreciate']):
            if context['sentiment'] == 'positive':
                return "😊 You're very welcome! I'm delighted I could help. Feel free to ask me anything else!"
            return "You're welcome! I'm here to help whenever you need assistance. 😊"
        
        # Help requests
        if any(word in query_lower for word in ['help', 'assist', 'support']):
            return """🤖 I'm here to help! I can assist with:

📁 **File Operations**: Create, read, write files and list directories
💻 **Programming**: Python, JavaScript, React, Flask, Git, APIs, databases  
🧠 **General Knowledge**: Science, technology, AI, space, health
💡 **Problem Solving**: Debug code, explain concepts, provide examples
🎯 **Task Execution**: Analysis, research, content generation

What would you like help with today?"""
        
        # About queries
        if context['is_question'] and any(word in query_lower for word in ['you', 'yourself', 'what are you']):
            return """🤖 I'm a free AI assistant that runs entirely on cloud infrastructure. Here's what makes me unique:

✨ **No API Keys Required**: I work without external AI service dependencies
🚀 **Fast Responses**: Instant replies using built-in knowledge base
🔒 **Privacy-Focused**: Your data stays secure, no external transmissions
💰 **Cost-Free**: No per-request charges or token limits
🛠️ **Versatile**: File operations, programming help, and general knowledge

I'm designed to be accessible, helpful, and reliable for all your needs!"""
        
        # Context-aware responses
        if context['is_question']:
            if context['urgency'] == 'high':
                return "⚡ I understand this is urgent! I'm ready to help you quickly. Could you provide more details about what you need?"
            elif context['sentiment'] == 'negative':
                return "😔 I can sense you might be frustrated. I'm here to help make things better. What specific issue can I assist you with?"
            elif context['sentiment'] == 'positive':
                return "😊 I'm glad you're in good spirits! I'd be happy to help. What question can I answer for you?"
            else:
                return "🤔 That's an interesting question! I'd be happy to help you explore that topic. Could you provide a bit more context about what you're looking for?"
        
        # Default response with sentiment consideration
        if context['sentiment'] == 'positive':
            return "😊 I appreciate your positive energy! Feel free to ask me questions or let me know how I can help you today."
        elif context['sentiment'] == 'negative':
            return "I understand. I'm here to help make things better. What can I assist you with?"
        else:
            return "💭 I'm listening and ready to help. Feel free to ask questions or let me know what you'd like to work on!"
    
    @staticmethod
    def generate_response(query: str, context: List[Dict] = None) -> str:
        """Main entry point for response generation with enhanced NLP"""
        responder = SmartResponder()
        analysis = responder.analyze_query_intent(query)
        return responder.generate_contextual_response(query, analysis, context)
        
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
        self.semantic_processor = SemanticQueryProcessor()  # Add semantic processor
        self.ml_processor = MLQueryUnderstanding()  # Add ML query understanding
        
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
        """Execute task with enhanced semantic understanding"""
        try:
            start_time = time.time()
            
            # Process query with semantic understanding
            semantic_analysis = self.semantic_processor.process_complex_query(task)
            
            # First try tool operations with expanded query
            tool_result = self._parse_and_execute_tools(semantic_analysis['expanded_query'])
            if not tool_result:
                # Try with original query if expanded didn't work
                tool_result = self._parse_and_execute_tools(task)
            
            if tool_result:
                # Enhance tool result with contextual information
                enhanced_result = self._enhance_tool_result(tool_result, semantic_analysis)
                self._update_conversation_history(task, enhanced_result)
                return {
                    "status": "completed",
                    "result": enhanced_result,
                    "type": "tool_operation",
                    "semantic_analysis": semantic_analysis,
                    "execution_time": round(time.time() - start_time, 2)
                }
            
            # Use enhanced response generation with semantic analysis
            result = self._generate_enhanced_response(task, semantic_analysis)
            
            # Update conversation history
            self._update_conversation_history(task, result)
            
            return {
                "status": "completed",
                "result": result,
                "type": "enhanced_semantic_response",
                "semantic_analysis": semantic_analysis,
                "execution_time": round(time.time() - start_time, 2)
            }
            
        except Exception as e:
            logger.error(f"Task execution error: {str(e)}")
            return {
                "status": "failed", 
                "error": f"I encountered an error: {str(e)}. Please try rephrasing your request.",
                "type": "error"
            }
    
    def _enhance_tool_result(self, tool_result: str, semantic_analysis: dict) -> str:
        """Enhance tool results with contextual information"""
        context_cues = semantic_analysis['context_cues']
        suggestions = semantic_analysis['processing_suggestions']
        
        enhanced_result = tool_result
        
        # Add contextual enhancements
        if context_cues['urgency']:
            enhanced_result += "\n\n⚡ **Quick Action Completed** - Task handled with priority!"
        
        if context_cues['complexity_level'] == 'simple' and 'step-by-step' in suggestions:
            enhanced_result += "\n\n💡 **Next Steps**: Let me know if you need help with the next part of your workflow."
        
        if context_cues['emotional_tone'] == 'frustrated':
            enhanced_result += "\n\n😊 **Here to Help**: I hope this resolved your issue! Feel free to ask if you need anything else."
        
        # Add suggestions for complex queries
        if semantic_analysis['complexity_score'] > 0.7:
            enhanced_result += f"\n\n🎯 **Advanced Query Detected** (complexity: {semantic_analysis['complexity_score']:.1f}) - I've processed your complex request thoroughly."
        
        return enhanced_result
    
    def _generate_enhanced_response(self, task: str, semantic_analysis: dict) -> str:
        """Generate response using enhanced semantic understanding"""
        context_cues = semantic_analysis['context_cues']
        combined_intents = semantic_analysis['combined_intents']
        advanced_entities = semantic_analysis['advanced_entities']
        
        # Handle combined intents (multi-step tasks)
        if combined_intents:
            return self._handle_combined_intents(task, combined_intents, context_cues, advanced_entities)
        
        # Use traditional response type detection enhanced with semantic analysis
        response_type = self._get_enhanced_response_type(task, advanced_entities)
        
        if response_type == "programming_help":
            result = self.knowledge.programming_help(task)
        elif response_type == "general_knowledge":
            result = self.knowledge.general_facts(task)
        elif response_type == "file_operation":
            result = self._generate_file_operation_guidance(task, context_cues)
        else:
            result = self.responder.generate_response(task, self.conversation_history)
        
        # Apply contextual enhancements
        return self._apply_contextual_enhancements(result, context_cues, semantic_analysis)
    
    def _handle_combined_intents(self, task: str, combined_intents: list, context_cues: dict, entities: dict) -> str:
        """Handle complex queries with multiple intents"""
        if 'create_and_populate' in combined_intents:
            return """🔧 **Multi-Step File Operation Detected**

I can help you create and populate a file in one go! Here's how:

**Format**: "Create a file called [filename] with [your content]"
**Example**: "Create a file called notes.txt with My important notes here"

The file will be created and populated with your specified content automatically."""

        elif 'read_and_analyze' in combined_intents:
            return """📊 **Read & Analysis Request Detected**

I can read a file and provide analysis! Here's what I can do:

1. **Read the file contents** - Display the full content
2. **Analyze the content** - Provide insights about structure, format, or data
3. **Summarize findings** - Give you key takeaways

**Example**: "Read example.txt and analyze its content"
Which file would you like me to read and analyze?"""

        elif 'compare_files' in combined_intents:
            return """⚖️ **File Comparison Request Detected**

I can help compare files! Here's my approach:

1. **Read both files** - Access the content of each file
2. **Compare structures** - Analyze differences in format and content
3. **Highlight key differences** - Point out important variations
4. **Provide recommendations** - Suggest which might be better for your needs

Which files would you like me to compare?"""

        elif 'backup_and_modify' in combined_intents:
            return """🛡️ **Backup & Modify Request Detected**

I can help with safe file modifications! Here's the process:

1. **Create backup** - Save a copy of the original file
2. **Apply modifications** - Make your requested changes
3. **Verify changes** - Confirm the modifications are correct
4. **Provide both versions** - Give you access to original and modified

What file would you like to backup and modify?"""

        return "🎯 I detected a complex multi-step request. Could you break it down into specific steps so I can help you more effectively?"
    
    def _get_enhanced_response_type(self, query: str, entities: dict) -> str:
        """Enhanced response type detection using semantic entities"""
        query_lower = query.lower()
        
        # Check advanced entities for better classification
        if entities['technologies']:
            tech_types = [tech[0] for tech in entities['technologies']]
            if any('programming' in tech_type or 'framework' in tech_type for tech_type in tech_types):
                return "programming_help"
        
        # Enhanced file operation detection
        if entities['file_types'] or any(keyword in query_lower for keyword in ["file", "read", "write", "create", "save", "directory", "folder", "list"]):
            return "file_operation"
        
        # Enhanced programming detection
        prog_keywords = ["python", "javascript", "html", "css", "react", "flask", "git", "api", "database", "code", "programming"]
        if any(keyword in query_lower for keyword in prog_keywords) or entities['technologies']:
            return "programming_help"
        
        # Enhanced knowledge detection
        knowledge_keywords = ["what is", "tell me about", "explain", "how does", "science", "technology", "ai", "space"]
        if any(keyword in query_lower for keyword in knowledge_keywords):
            return "general_knowledge"
        
        return "general_chat"
    
    def _generate_file_operation_guidance(self, task: str, context_cues: dict) -> str:
        """Generate enhanced file operation guidance"""
        base_guidance = """🔧 **File Operations Available:**

• **Create file**: "Create a file called example.txt with Hello World"
• **Read file**: "Read the file example.txt" or "Show me example.txt"  
• **List files**: "List directory" or "Show me the files"

Try one of these commands or ask for help with specific file operations!"""

        if context_cues['urgency']:
            return "⚡ **Quick File Operations Help**\n\n" + base_guidance + "\n\n🚀 I'll process your file operation immediately once you specify what you need!"
        
        if context_cues['complexity_level'] == 'simple':
            return "📁 **Simple File Operations**\n\n" + base_guidance + "\n\n💡 **Tip**: Start with something simple like 'list files' to see what's available!"
        
        if context_cues['emotional_tone'] == 'frustrated':
            return "😊 **I'm Here to Help with Files**\n\n" + base_guidance + "\n\n🤗 Don't worry - file operations are straightforward once you get the hang of it!"
        
        return base_guidance
    
    def _apply_contextual_enhancements(self, result: str, context_cues: dict, semantic_analysis: dict) -> str:
        """Apply contextual enhancements to any response"""
        enhanced_result = result
        
        # Add complexity-appropriate additions
        if context_cues['complexity_level'] == 'step_by_step':
            enhanced_result += "\n\n📋 **Step-by-Step Guide Available**: Ask me to break this down into detailed steps if needed!"
        
        if context_cues['uncertainty']:
            enhanced_result += "\n\n🤝 **Need More Help?**: I can provide more detailed explanations or examples - just ask!"
        
        if context_cues['preference']:
            enhanced_result += "\n\n⭐ **Customizable**: Let me know your specific preferences and I can tailor my approach!"
        
        # Add processing insights for complex queries
        if semantic_analysis['complexity_score'] > 0.5:
            suggestions = semantic_analysis['processing_suggestions']
            if suggestions:
                enhanced_result += f"\n\n🧠 **Processing Notes**: {', '.join(suggestions[:2])}"
        
        return enhanced_result
class SemanticQueryProcessor:
    """Advanced semantic query processing for better understanding"""
    
    def __init__(self):
        """Initialize with semantic patterns and word embeddings simulation"""
        # Synonym mappings for better understanding
        self.synonym_map = {
            # File operations
            'create': ['make', 'generate', 'build', 'craft', 'produce', 'establish'],
            'read': ['view', 'display', 'show', 'open', 'examine', 'check'],
            'write': ['save', 'store', 'record', 'document', 'input'],
            'delete': ['remove', 'erase', 'eliminate', 'destroy', 'wipe'],
            'list': ['enumerate', 'catalog', 'inventory', 'display', 'show'],
            
            # Programming concepts
            'explain': ['describe', 'clarify', 'elaborate', 'detail', 'illustrate'],
            'debug': ['fix', 'troubleshoot', 'resolve', 'repair', 'correct'],
            'optimize': ['improve', 'enhance', 'refine', 'streamline', 'perfect'],
            'example': ['sample', 'demonstration', 'instance', 'illustration', 'template'],
            
            # General concepts
            'analyze': ['examine', 'study', 'investigate', 'assess', 'evaluate'],
            'compare': ['contrast', 'differentiate', 'distinguish', 'relate'],
            'learn': ['understand', 'grasp', 'comprehend', 'master', 'acquire'],
            'help': ['assist', 'support', 'aid', 'guide', 'advise']
        }
        
        # Contextual phrase patterns for complex understanding
        self.contextual_patterns = {
            'uncertainty': [
                r'not sure (?:how|what|why|when|where)',
                r'don\'?t know (?:how|what|why|when|where)',
                r'confused about',
                r'having trouble with',
                r'struggling to understand',
                r'can\'?t figure out'
            ],
            'urgency': [
                r'need (?:this|to) (?:asap|quickly|fast|now|immediately)',
                r'urgent(?:ly)? need',
                r'time(?:-)?sensitive',
                r'deadline (?:is|approaching)',
                r'rush(?:ing)? to',
                r'critical(?:ly)? important'
            ],
            'preference': [
                r'prefer(?:ably)?',
                r'would (?:rather|like)',
                r'best (?:way|approach|method)',
                r'recommend(?:ed)? (?:way|approach|method)',
                r'suggest(?:ed)? (?:way|approach|method)'
            ],
            'complexity_level': [
                r'(?:simple|easy|basic|beginner) (?:way|approach|method|explanation)',
                r'(?:advanced|complex|detailed|in-depth) (?:way|approach|method|explanation)',
                r'step(?:-)?by(?:-)?step',
                r'comprehensive (?:guide|explanation)',
                r'quick (?:overview|summary)'
            ]
        }
        
        # Multi-word entity recognition patterns
        self.entity_patterns = {
            'file_extensions': r'\.(?:txt|py|js|html|css|json|xml|csv|md|yml|yaml|conf|cfg|ini|log)(?:\s|$)',
            'programming_frameworks': r'(?:react|angular|vue|django|flask|express|spring|laravel|rails)(?:\s|$)',
            'databases': r'(?:mysql|postgresql|mongodb|redis|sqlite|oracle|sql server)(?:\s|$)',
            'cloud_platforms': r'(?:aws|azure|gcp|heroku|render|vercel|netlify|digital ocean)(?:\s|$)',
            'version_control': r'(?:git|github|gitlab|bitbucket|svn)(?:\s|$)',
            'package_managers': r'(?:npm|pip|yarn|composer|maven|gradle)(?:\s|$)'
        }
        
        # Intent combination patterns for complex queries
        self.combined_intent_patterns = {
            'create_and_populate': [
                r'create.*(?:file|document).*(?:with|containing|that has)',
                r'make.*(?:file|document).*(?:with|containing|that has)',
                r'generate.*(?:file|document).*(?:with|containing|that has)'
            ],
            'read_and_analyze': [
                r'(?:read|open|show).*(?:file|document).*(?:and|then).*(?:analyze|examine|check)',
                r'(?:analyze|examine|check).*(?:file|document|content)',
                r'what(?:\'s| is).*in.*(?:file|document)'
            ],
            'compare_files': [
                r'(?:compare|difference between).*(?:files?|documents?)',
                r'(?:files?|documents?).*(?:vs|versus|compared to)',
                r'which.*(?:file|document).*(?:better|different)'
            ],
            'backup_and_modify': [
                r'(?:backup|copy).*(?:file|document).*(?:and|then).*(?:modify|change|edit)',
                r'(?:save|create).*(?:copy|backup).*(?:before|then).*(?:modifying|changing|editing)'
            ]
        }
    
    def expand_query_with_synonyms(self, query: str) -> str:
        """Expand query with synonyms for better matching"""
        words = query.lower().split()
        expanded_words = []
        
        for word in words:
            # Check if word is a key in synonym map
            if word in self.synonym_map:
                # Add original word and top synonym
                expanded_words.append(word)
                if self.synonym_map[word]:
                    expanded_words.append(self.synonym_map[word][0])
            else:
                # Check if word is a synonym of any key
                for key, synonyms in self.synonym_map.items():
                    if word in synonyms:
                        expanded_words.append(key)
                        break
                expanded_words.append(word)
        
        return ' '.join(expanded_words)
    
    def extract_contextual_cues(self, query: str) -> dict:
        """Extract contextual information from query"""
        cues = {
            'uncertainty': False,
            'urgency': False,
            'preference': False,
            'complexity_level': 'normal',
            'emotional_tone': 'neutral'
        }
        
        query_lower = query.lower()
        
        # Check for contextual patterns
        for context_type, patterns in self.contextual_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    if context_type == 'complexity_level':
                        if 'simple' in pattern or 'easy' in pattern or 'basic' in pattern or 'beginner' in pattern:
                            cues['complexity_level'] = 'simple'
                        elif 'advanced' in pattern or 'complex' in pattern or 'detailed' in pattern:
                            cues['complexity_level'] = 'advanced'
                        elif 'step' in pattern:
                            cues['complexity_level'] = 'step_by_step'
                    else:
                        cues[context_type] = True
                    break
        
        # Emotional tone detection
        frustration_words = ['frustrated', 'annoyed', 'stuck', 'confused', 'lost', 'helpless']
        excitement_words = ['excited', 'eager', 'enthusiastic', 'awesome', 'amazing', 'great']
        
        if any(word in query_lower for word in frustration_words):
            cues['emotional_tone'] = 'frustrated'
        elif any(word in query_lower for word in excitement_words):
            cues['emotional_tone'] = 'excited'
        
        return cues
    
    def detect_combined_intents(self, query: str) -> list:
        """Detect complex queries with multiple intents"""
        detected_intents = []
        query_lower = query.lower()
        
        for intent_combo, patterns in self.combined_intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    detected_intents.append(intent_combo)
                    break
        
        return detected_intents
    
    def extract_advanced_entities(self, query: str) -> dict:
        """Extract complex entities using advanced patterns"""
        entities = {
            'technologies': [],
            'file_types': [],
            'specific_terms': [],
            'numbers': [],
            'time_references': []
        }
        
        # Technology extraction
        for entity_type, pattern in self.entity_patterns.items():
            matches = re.findall(pattern, query.lower())
            if matches:
                entities['technologies'].extend([(entity_type, match.strip('.')) for match in matches])
        
        # File extensions
        file_matches = re.findall(r'\.([a-zA-Z0-9]+)', query)
        entities['file_types'].extend(file_matches)
        
        # Numbers
        number_matches = re.findall(r'\b\d+\b', query)
        entities['numbers'].extend(number_matches)
        
        # Time references
        time_patterns = [r'(?:today|tomorrow|yesterday)', r'(?:this|next|last)\s+(?:week|month|year)', r'\d+\s+(?:minutes?|hours?|days?)']
        for pattern in time_patterns:
            time_matches = re.findall(pattern, query.lower())
            entities['time_references'].extend(time_matches)
        
        return entities
    
    def process_complex_query(self, query: str) -> dict:
        """Process query with full semantic understanding"""
        # Expand with synonyms
        expanded_query = self.expand_query_with_synonyms(query)
        
        # Extract contextual cues
        context_cues = self.extract_contextual_cues(query)
        
        # Detect combined intents
        combined_intents = self.detect_combined_intents(query)
        
        # Extract advanced entities
        advanced_entities = self.extract_advanced_entities(query)
        
        # Query complexity analysis
        complexity_score = self._calculate_complexity_score(query)
        
        return {
            'original_query': query,
            'expanded_query': expanded_query,
            'context_cues': context_cues,
            'combined_intents': combined_intents,
            'advanced_entities': advanced_entities,
            'complexity_score': complexity_score,
            'processing_suggestions': self._generate_processing_suggestions(context_cues, combined_intents)
        }
    
    def _calculate_complexity_score(self, query: str) -> float:
        """Calculate query complexity score (0-1)"""
        factors = {
            'length': min(len(query.split()) / 20, 1.0) * 0.3,
            'question_words': len([w for w in query.lower().split() if w in ['what', 'how', 'why', 'when', 'where', 'which']]) / 10 * 0.2,
            'technical_terms': len(re.findall(r'(?:python|javascript|api|database|server|framework|library)', query.lower())) / 5 * 0.3,
            'conditional_logic': len(re.findall(r'(?:if|when|unless|provided|assuming|given)', query.lower())) / 3 * 0.2
        }
        
        return min(sum(factors.values()), 1.0)
    
    def _generate_processing_suggestions(self, context_cues: dict, combined_intents: list) -> list:
        """Generate suggestions for processing the query"""
        suggestions = []
        
        if context_cues['uncertainty']:
            suggestions.append("Provide clear, step-by-step guidance")
            suggestions.append("Include examples and explanations")
        
        if context_cues['urgency']:
            suggestions.append("Prioritize quick, actionable solutions")
            suggestions.append("Provide direct answers first, details second")
        
        if context_cues['complexity_level'] == 'simple':
            suggestions.append("Use simple language and basic concepts")
            suggestions.append("Avoid technical jargon")
        elif context_cues['complexity_level'] == 'advanced':
            suggestions.append("Provide detailed technical information")
            suggestions.append("Include advanced concepts and best practices")
        
        if combined_intents:
            suggestions.append("Handle multiple tasks in sequence")
            suggestions.append("Provide comprehensive solution covering all aspects")
        
        if context_cues['emotional_tone'] == 'frustrated':
            suggestions.append("Use empathetic and supportive language")
            suggestions.append("Provide reassurance and clear next steps")
        
        return suggestions

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

class MLQueryUnderstanding:
    """Machine Learning-based query understanding using lightweight models"""
    
    def __init__(self):
        """Initialize ML-based understanding without heavy dependencies"""
        # Simulated word embeddings using similarity scores
        self.word_similarity_matrix = {
            'create': {'make': 0.9, 'build': 0.8, 'generate': 0.85, 'produce': 0.75},
            'read': {'view': 0.9, 'display': 0.85, 'show': 0.8, 'examine': 0.7},
            'write': {'save': 0.9, 'store': 0.85, 'record': 0.8, 'document': 0.7},
            'explain': {'describe': 0.9, 'clarify': 0.85, 'elaborate': 0.8, 'detail': 0.75},
            'help': {'assist': 0.9, 'support': 0.85, 'aid': 0.8, 'guide': 0.75}
        }
        
        # Intent classification patterns with confidence scores
        self.intent_classifiers = {
            'file_operations': {
                'keywords': ['file', 'directory', 'folder', 'document', 'path', 'create', 'read', 'write', 'delete', 'list'],
                'phrases': ['file operation', 'manage files', 'work with files', 'file system'],
                'weight': 1.0
            },
            'programming_help': {
                'keywords': ['code', 'programming', 'python', 'javascript', 'html', 'css', 'debug', 'function', 'variable', 'class'],
                'phrases': ['help with code', 'programming question', 'coding problem', 'software development'],
                'weight': 1.0
            },
            'general_knowledge': {
                'keywords': ['what', 'how', 'why', 'explain', 'tell me', 'information', 'learn', 'understand', 'knowledge'],
                'phrases': ['tell me about', 'what is', 'how does', 'general information'],
                'weight': 0.8
            },
            'task_execution': {
                'keywords': ['analyze', 'research', 'generate', 'create', 'optimize', 'improve', 'task', 'work'],
                'phrases': ['help me with', 'work on', 'execute task', 'perform action'],
                'weight': 0.9
            }
        }
        
        # Context understanding patterns
        self.context_patterns = {
            'temporal': {
                'urgent': ['urgent', 'asap', 'quickly', 'immediately', 'rush', 'fast', 'now'],
                'future': ['later', 'eventually', 'someday', 'in the future', 'when I have time'],
                'scheduled': ['today', 'tomorrow', 'this week', 'next month', 'deadline']
            },
            'complexity': {
                'simple': ['simple', 'easy', 'basic', 'quick', 'straightforward', 'brief'],
                'detailed': ['detailed', 'comprehensive', 'thorough', 'complete', 'in-depth'],
                'step_by_step': ['step by step', 'walk me through', 'guide me', 'tutorial']
            },
            'emotional': {
                'frustrated': ['stuck', 'confused', 'lost', 'frustrated', 'having trouble', 'can\'t figure out'],
                'excited': ['excited', 'eager', 'love to', 'can\'t wait', 'awesome', 'amazing'],
                'uncertain': ['not sure', 'maybe', 'possibly', 'might', 'unclear', 'unsure']
            }
        }
        
        # Advanced entity extraction patterns
        self.entity_extractors = {
            'file_paths': r'(?:[a-zA-Z0-9_\-./\\]+\.(?:txt|py|js|html|css|json|xml|csv|md|yml|yaml|conf|cfg|ini|log))',
            'urls': r'https?://(?:[-\w.])+(?::[0-9]+)?(?:/(?:[\w/_.])*)?(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?',
            'code_snippets': r'```[\s\S]*?```|`[^`]+`',
            'version_numbers': r'v?\d+\.\d+(?:\.\d+)?',
            'file_sizes': r'\d+(?:\.\d+)?\s*(?:B|KB|MB|GB|TB)',
            'programming_languages': r'\b(?:python|javascript|java|c\+\+|c#|php|ruby|go|rust|swift|kotlin)\b',
            'frameworks': r'\b(?:react|angular|vue|django|flask|express|spring|rails|laravel)\b'
        }
    
    def calculate_semantic_similarity(self, word1: str, word2: str) -> float:
        """Calculate semantic similarity between two words"""
        word1, word2 = word1.lower(), word2.lower()
        
        # Direct similarity lookup
        if word1 in self.word_similarity_matrix and word2 in self.word_similarity_matrix[word1]:
            return self.word_similarity_matrix[word1][word2]
        if word2 in self.word_similarity_matrix and word1 in self.word_similarity_matrix[word2]:
            return self.word_similarity_matrix[word2][word1]
        
        # Character-based similarity for unknown words
        return self._calculate_edit_distance_similarity(word1, word2)
    
    def _calculate_edit_distance_similarity(self, word1: str, word2: str) -> float:
        """Calculate similarity based on edit distance"""
        if len(word1) == 0 or len(word2) == 0:
            return 0.0
        
        # Simple edit distance calculation
        max_len = max(len(word1), len(word2))
        edit_distance = sum(c1 != c2 for c1, c2 in zip(word1, word2)) + abs(len(word1) - len(word2))
        
        return max(0, 1 - (edit_distance / max_len))
    
    def classify_intent_with_ml(self, query: str) -> dict:
        """Classify intent using ML-like approach with confidence scores"""
        query_lower = query.lower()
        intent_scores = {}
        
        for intent, patterns in self.intent_classifiers.items():
            score = 0.0
            
            # Keyword matching with semantic similarity
            for keyword in patterns['keywords']:
                for word in query_lower.split():
                    similarity = self.calculate_semantic_similarity(keyword, word)
                    if similarity > 0.7:  # Threshold for similarity
                        score += similarity * patterns['weight']
            
            # Phrase matching
            for phrase in patterns['phrases']:
                if phrase in query_lower:
                    score += 1.0 * patterns['weight']
            
            # Normalize score
            intent_scores[intent] = min(score / len(patterns['keywords']), 1.0)
        
        # Get top intent with confidence
        if intent_scores:
            top_intent = max(intent_scores, key=intent_scores.get)
            confidence = intent_scores[top_intent]
            
            return {
                'intent': top_intent,
                'confidence': confidence,
                'all_scores': intent_scores
            }
        
        return {
            'intent': 'general_chat',
 'confidence': 0.5,
            'all_scores': {'general_chat': 0.5}
        }
    
    def extract_context_with_ml(self, query: str) -> dict:
        """Extract context using ML-like pattern recognition"""
        query_lower = query.lower()
        context = {
            'temporal_urgency': 'normal',
            'complexity_preference': 'normal',
            'emotional_state': 'neutral',
            'confidence_scores': {}
        }
        
        for context_type, categories in self.context_patterns.items():
            category_scores = {}
            
            for category, patterns in categories.items():
                score = 0.0
                for pattern in patterns:
                    if pattern in query_lower:
                        score += 1.0
                    # Check for partial matches with semantic similarity
                    for word in query_lower.split():
                        for pattern_word in pattern.split():
                            similarity = self.calculate_semantic_similarity(pattern_word, word)
                            if similarity > 0.8:
                                score += similarity * 0.5
                
                category_scores[category] = score
            
            # Assign the highest scoring category
            if category_scores:
                top_category = max(category_scores, key=category_scores.get)
                if category_scores[top_category] > 0:
                    if context_type == 'temporal':
                        context['temporal_urgency'] = top_category
                    elif context_type == 'complexity':
                        context['complexity_preference'] = top_category
                    elif context_type == 'emotional':
                        context['emotional_state'] = top_category
                    
                    context['confidence_scores'] = category_scores
        
        return context
    
    def extract_entities_with_ml(self, query: str) -> dict:
        """Extract entities using advanced pattern recognition"""
        entities = {
            'files': [],
            'urls': [],
            'code_snippets': [],
            'technical_terms': [],
            'metrics': []
        }
        
        # Extract using regex patterns
        for entity_type, pattern in self.entity_extractors.items():
            matches = re.findall(pattern, query, re.IGNORECASE)
            if matches:
                if entity_type == 'file_paths':
                    entities['files'].extend(matches)
                elif entity_type == 'urls':
                    entities['urls'].extend(matches)
                elif entity_type == 'code_snippets':
                    entities['code_snippets'].extend(matches)
                elif entity_type in ['programming_languages', 'frameworks']:
                    entities['technical_terms'].extend(matches)
                elif entity_type in ['version_numbers', 'file_sizes']:
                    entities['metrics'].extend(matches)
        
        return entities
    
    def generate_ml_enhanced_response_strategy(self, query: str) -> dict:
        """Generate response strategy using ML analysis"""
        # Classify intent
        intent_analysis = self.classify_intent_with_ml(query)
        
        # Extract context
        context_analysis = self.extract_context_with_ml(query)
        
        # Extract entities
        entity_analysis = self.extract_entities_with_ml(query)
        
        # Generate response strategy
        strategy = {
            'personalization_level': 'high',
            'adjust_complexity': self.user_profile['technical_level'],
            'preferred_style': self.user_profile['preferred_style'],
            'common_pattern': self._identify_common_pattern(query),
            'success_optimization': self._suggest_success_optimizations()
        }
        
        return {
            'intent': intent_analysis,
            'context': context_analysis,
            'entities': entity_analysis,
            'strategy': strategy
        }
    
    def _determine_primary_approach(self, intent_analysis: dict, context_analysis: dict) -> str:
        """Determine the primary approach for responding"""
        intent = intent_analysis['intent']
        confidence = intent_analysis['confidence']
        urgency = context_analysis['temporal_urgency']
        
        if confidence > 0.8:
            if urgency == 'urgent':
                return f"direct_{intent}"
            else:
                return f"comprehensive_{intent}"
        elif confidence > 0.5:
            return f"guided_{intent}"
        else:
            return "exploratory_chat"
    
    def _determine_response_tone(self, context_analysis: dict) -> str:
        """Determine appropriate response tone"""
        emotional_state = context_analysis['emotional_state']
        urgency = context_analysis['temporal_urgency']
        
        if emotional_state == 'frustrated':
            return "supportive_empathetic"
        elif emotional_state == 'excited':
            return "enthusiastic_encouraging"
        elif urgency == 'urgent':
            return "efficient_direct"
        else:
            return "friendly_professional"
    
    def _determine_content_depth(self, context_analysis: dict) -> str:
        """Determine appropriate content depth"""
        complexity = context_analysis['complexity_preference']
        
        if complexity == 'simple':
            return "concise_basic"
        elif complexity == 'detailed':
            return "comprehensive_advanced"
        elif complexity == 'step_by_step':
            return "structured_tutorial"
        else:
            return "balanced_informative"
    
    def _determine_personalization(self, context_analysis: dict, entity_analysis: dict) -> dict:
        """Determine personalization elements"""
        return {
            'use_examples': len(entity_analysis['technical_terms']) > 0,
            'reference_user_context': context_analysis['emotional_state'] != 'neutral',
            'adapt_complexity': context_analysis['complexity_preference'] != 'normal',
            'prioritize_efficiency': context_analysis['temporal_urgency'] == 'urgent'
        }
    
    def _generate_follow_up_suggestions(self, intent_analysis: dict, entity_analysis: dict) -> list:
        """Generate intelligent follow-up suggestions"""
        suggestions = []
        intent = intent_analysis['intent']
        
        if intent == 'file_operations' and entity_analysis['files']:
            suggestions.extend([
                "Would you like me to help with additional file operations?",
                "Do you need to perform batch operations on multiple files?",
                "Should I help you organize or backup these files?"
            ])
        elif intent == 'programming_help' and entity_analysis['technical_terms']:
            suggestions.extend([
                "Would you like to see more examples or best practices?",
                "Do you need help with debugging or optimization?",
                "Should I explain related concepts or advanced techniques?"
            ])
        elif intent == 'general_knowledge':
            suggestions.extend([
                "Would you like me to dive deeper into any specific aspect?",
                "Are you interested in related topics or practical applications?",
                "Do you need examples or real-world use cases?"
            ])
        
        return suggestions[:3]  # Limit to top 3 suggestions
    def _update_conversation_history(self, user_input: str, response: str):
        """Update conversation history with the latest interaction"""
        try:
            conversation_entry = {
                "user": user_input,
                "assistant": response,
                "timestamp": time.time()
            }
            
            self.conversation_history.append(conversation_entry)
            
            # Maintain conversation window
            if len(self.conversation_history) > self.max_history:
                self.conversation_history = self.conversation_history[-self.max_history:]
                
            logger.debug(f"Updated conversation history. Total entries: {len(self.conversation_history)}")
            
        except Exception as e:
            logger.error(f"Error updating conversation history: {str(e)}")
            # Don't let this error break the main functionality
            pass