"""
Free Autonomous AI Agent - Render Deployment Ready

Lightweight version optimized for cloud deployment
Now includes FREE LLM capabilities using Hugging Face models
"""

import os
import logging
import json
import re
import time
from typing import Dict, Any, List
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS

# Check if transformers is available for free LLM
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    import torch
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    print("⚠️ Transformers not available - using pattern-based responses")

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
            "date": "June 30, 2025",
            "system": "Free AI Agent - Lightweight Cloud Version with LLM",
            "capabilities": "File operations, general conversation, programming help, knowledge base, free LLM"
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
    
    @staticmethod
    def generate_response(query: str, context: List[Dict] = None) -> str:
        """Main entry point for response generation with enhanced NLP"""
        responder = SmartResponder()
        analysis = responder.analyze_query_intent(query)
        return responder.generate_contextual_response(query, analysis, context)

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
        query_lower = query.lower()
        
        # Gratitude responses
        if any(word in query_lower for word in ['thank', 'thanks', 'appreciate']):
            return "😊 You're very welcome! I'm delighted I could help. Feel free to ask me anything else!"
        
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
        if analysis['context']['is_question'] and any(word in query_lower for word in ['you', 'yourself', 'what are you']):
            return """🤖 I'm a free AI assistant with LLM capabilities! Here's what makes me unique:

✨ **Free LLM Integration**: Enhanced with Hugging Face models for natural conversation
🚀 **Fast Responses**: Intelligent responses with contextual understanding
🔒 **Privacy-Focused**: Your data stays secure, no external transmissions
💰 **Cost-Free**: No per-request charges or token limits
🛠️ **Versatile**: File operations, programming help, and general knowledge

I'm designed to be accessible, helpful, and reliable for all your needs!"""
        
        return "💭 I'm listening and ready to help. Feel free to ask questions or let me know what you'd like to work on!"

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

class SemanticQueryProcessor:
    """Advanced semantic query processing for better understanding"""
    
    def __init__(self):
        """Initialize with semantic patterns and word embeddings simulation"""
        # Synonym mappings for better understanding
        self.synonym_map = {
            'create': ['make', 'generate', 'build', 'craft', 'produce', 'establish'],
            'read': ['view', 'display', 'show', 'open', 'examine', 'check'],
            'write': ['save', 'store', 'record', 'document', 'input'],
            'delete': ['remove', 'erase', 'eliminate', 'destroy', 'wipe'],
            'list': ['enumerate', 'catalog', 'inventory', 'display', 'show'],
        }
        
        # Intent combination patterns for complex queries
        self.combined_intent_patterns = {
            'create_and_populate': [
                r'create.*(?:file|document).*(?:with|containing|that has)',
                r'make.*(?:file|document).*(?:with|containing|that has)',
                r'generate.*(?:file|document).*(?:with|containing|that has)'
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
                expanded_words.append(word)
        
        return ' '.join(expanded_words)
    
    def extract_contextual_cues(self, query: str) -> dict:
        """Extract contextual information from query"""
        return {
            'uncertainty': False,
            'urgency': False,
            'preference': False,
            'complexity_level': 'normal',
            'emotional_tone': 'neutral'
        }
    
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
        
        # File extensions
        file_matches = re.findall(r'\.([a-zA-Z0-9]+)', query)
        entities['file_types'].extend(file_matches)
        
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
        complexity_score = min(len(query.split()) / 20, 1.0) * 0.5
        
        return {
            'original_query': query,
            'expanded_query': expanded_query,
            'context_cues': context_cues,
            'combined_intents': combined_intents,
            'advanced_entities': advanced_entities,
            'complexity_score': complexity_score,
            'processing_suggestions': []
        }

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

class FreeLLMAgent:
    """Free LLM Agent using Hugging Face models for enhanced responses"""
    
    def __init__(self):
        """Initialize free LLM with graceful fallback"""
        self.model_name = "microsoft/DialoGPT-small"  # Lightweight model for cloud deployment
        self.generator = None
        self.fallback_mode = True
        
        if HF_AVAILABLE:
            self._init_model()
        else:
            logger.info("📝 Using pattern-based responses (transformers not available)")
    
    def _init_model(self):
        """Initialize the Hugging Face model"""
        try:
            logger.info(f"🤖 Loading free LLM model: {self.model_name}")
            
            # Use a lightweight model for text generation
            self.generator = pipeline(
                "text-generation",
                model=self.model_name,
                device=-1,  # Use CPU (free)
                max_length=512,
                do_sample=True,
                temperature=0.7,
                pad_token_id=50256  # Set pad token to avoid warnings
            )
            
            logger.info("✅ Free LLM model loaded successfully!")
            self.fallback_mode = False
            
        except Exception as e:
            logger.warning(f"⚠️ Model loading failed: {e}")
            logger.info("🔄 Using intelligent fallback mode")
            self.fallback_mode = True
    
    def generate_llm_response(self, query: str, context: str = "") -> str:
        """Generate response using free LLM or intelligent fallback"""
        if not self.fallback_mode and self.generator:
            try:
                # Create a well-structured prompt for the LLM
                prompt = self._create_prompt(query, context)
                
                # Generate response using Hugging Face model
                response = self.generator(
                    prompt, 
                    max_length=len(prompt.split()) + 100,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=50256
                )
                
                # Extract the AI response
                generated_text = response[0]['generated_text']
                ai_response = generated_text.replace(prompt, "").strip()
                
                # Clean up the response
                ai_response = self._clean_response(ai_response)
                
                if ai_response and len(ai_response) > 10:
                    return f"🤖 **Free LLM Response**:\n{ai_response}"
                else:
                    return self._fallback_response(query)
                    
            except Exception as e:
                logger.warning(f"⚠️ LLM generation failed: {e}")
                return self._fallback_response(query)
        else:
            return self._fallback_response(query)
    
    def _create_prompt(self, query: str, context: str = "") -> str:
        """Create a well-structured prompt for the LLM"""
        system_context = """You are a helpful AI assistant that provides clear, concise, and accurate responses. 
You specialize in programming, technology, and general knowledge questions."""
        
        if context:
            prompt = f"{system_context}\n\nContext: {context}\n\nHuman: {query}\nAI:"
        else:
            prompt = f"{system_context}\n\nHuman: {query}\nAI:"
        
        return prompt
    
    def _clean_response(self, response: str) -> str:
        """Clean and format the LLM response"""
        # Remove common artifacts
        response = response.replace("Human:", "").replace("AI:", "")
        
        # Remove repetitive patterns
        lines = response.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            if line and line not in cleaned_lines[-3:]:  # Avoid immediate repetition
                cleaned_lines.append(line)
        
        response = '\n'.join(cleaned_lines)
        
        # Limit length for cloud deployment
        if len(response) > 500:
            response = response[:497] + "..."
        
        return response.strip()
    
    def _fallback_response(self, query: str) -> str:
        """Intelligent fallback when LLM is not available"""
        query_lower = query.lower()
        
        # Programming-related queries
        if any(keyword in query_lower for keyword in ['python', 'javascript', 'code', 'programming', 'function']):
            return """💻 **Programming Assistance**

I can help with programming questions! For the best experience with code generation and detailed explanations, the system can use free Hugging Face models when available.

**Current capabilities:**
• Code examples and snippets
• Programming concept explanations  
• Debugging guidance
• Best practices

What specific programming topic would you like help with?"""

        # General knowledge queries
        elif any(keyword in query_lower for keyword in ['what is', 'explain', 'how does', 'tell me about']):
            return """🧠 **Knowledge Assistant**

I'm here to help explain concepts and answer questions! While I can provide good responses using pattern matching, the system works even better with free LLM models for more natural conversations.

**I can help with:**
• Technology and science topics
• Programming and development
• General knowledge questions
• Step-by-step explanations

What would you like to learn about?"""

        # Default intelligent response
        else:
            return f"""🤖 **Free AI Assistant**

I understand you're asking about: "{query}"

**Enhanced Mode Available:** This system can use free Hugging Face models for more natural and detailed responses when the transformers library is installed.

**Current Mode:** Pattern-based responses with intelligent fallbacks

**I can still help with:**
• File operations and management
• Programming questions and examples
• General knowledge and explanations
• Technical problem solving

How can I assist you further?"""

class LightweightAIAgent:
    """Lightweight AI Agent optimized for cloud deployment with FREE LLM capabilities"""
    
    def __init__(self):
        """Initialize agent with knowledge base and free LLM"""
        self.file_ops = FileOperations()
        self.knowledge = GeneralKnowledge()
        self.responder = SmartResponder()
        self.semantic_processor = SemanticQueryProcessor()
        self.ml_processor = MLQueryUnderstanding()
        
        # Initialize Free LLM Agent
        self.free_llm = FreeLLMAgent()
        
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
        
        # LLM usage settings
        self.use_llm_for_complex_queries = True
        self.llm_complexity_threshold = 0.6
        
        logger.info("✅ Lightweight AI Agent with Free LLM initialized successfully")
    
    def _should_use_llm(self, query: str, semantic_analysis: dict) -> bool:
        """Determine if we should use LLM for this query"""
        if not self.use_llm_for_complex_queries or self.free_llm.fallback_mode:
            return False
        
        # Use LLM for complex queries
        complexity_score = semantic_analysis.get('complexity_score', 0)
        if complexity_score > self.llm_complexity_threshold:
            return True
        
        # Use LLM for conversational queries that aren't tool operations
        query_lower = query.lower()
        tool_keywords = ['file', 'read', 'write', 'create', 'save', 'directory', 'folder', 'list']
        is_tool_query = any(keyword in query_lower for keyword in tool_keywords)
        
        if not is_tool_query and len(query.split()) > 5:
            return True
        
        # Use LLM for questions that benefit from natural language generation
        question_indicators = ['how do i', 'can you explain', 'what would you recommend', 'help me understand']
        if any(indicator in query_lower for indicator in question_indicators):
            return True
        
        return False

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
                "result": f"I encountered an error: {str(e)}. Please try rephrasing your request.",
                "type": "error"
            }

    def _generate_enhanced_response(self, task: str, semantic_analysis: dict) -> str:
        """Generate response using enhanced semantic understanding with optional LLM"""
        context_cues = semantic_analysis['context_cues']
        combined_intents = semantic_analysis['combined_intents']
        advanced_entities = semantic_analysis['advanced_entities']
        
        # Check if we should use LLM for this query
        if self._should_use_llm(task, semantic_analysis):
            # Create context for LLM
            context_info = f"User context: {context_cues}, Entities: {advanced_entities}"
            llm_response = self.free_llm.generate_llm_response(task, context_info)
            
            # Apply contextual enhancements to LLM response
            return self._apply_contextual_enhancements(llm_response, context_cues, semantic_analysis)
        
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

        return "🎯 I detected a complex multi-step request. Could you break it down into specific steps so I can help you more effectively?"
    
    def _get_enhanced_response_type(self, query: str, entities: dict) -> str:
        """Enhanced response type detection using semantic entities"""
        query_lower = query.lower()
        
        # Enhanced file operation detection
        if entities.get('file_types') or any(keyword in query_lower for keyword in ["file", "read", "write", "create", "save", "directory", "folder", "list"]):
            return "file_operation"
        
        # Enhanced programming detection
        prog_keywords = ["python", "javascript", "html", "css", "react", "flask", "git", "api", "database", "code", "programming"]
        if any(keyword in query_lower for keyword in prog_keywords) or entities.get('technologies'):
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

Try one of these commands or ask me anything!"""

        if context_cues.get('urgency'):
            return "⚡ **Quick File Operations Help**\n\n" + base_guidance + "\n\n🚀 I'll process your file operation immediately once you specify what you need!"
        
        return base_guidance
    
    def _apply_contextual_enhancements(self, result: str, context_cues: dict, semantic_analysis: dict) -> str:
        """Apply contextual enhancements to any response"""
        enhanced_result = result
        
        # Add complexity-appropriate additions
        if context_cues.get('complexity_level') == 'step_by_step':
            enhanced_result += "\n\n📋 **Step-by-Step Guide Available**: Ask me to break this down into detailed steps if needed!"
        
        if context_cues.get('uncertainty'):
            enhanced_result += "\n\n🤝 **Need More Help?**: I can provide more detailed explanations or examples - just ask!"
        
        return enhanced_result

    def _enhance_tool_result(self, tool_result: str, semantic_analysis: dict) -> str:
        """Enhance tool results with contextual information"""
        context_cues = semantic_analysis['context_cues']
        enhanced_result = tool_result
        
        # Add contextual enhancements
        if context_cues.get('urgency'):
            enhanced_result += "\n\n⚡ **Quick Action Completed** - Task handled with priority!"
        
        if context_cues.get('emotional_tone') == 'frustrated':
            enhanced_result += "\n\n😊 **Here to Help**: I hope this resolved your issue! Feel free to ask if you need anything else."
        
        return enhanced_result

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
                
        except Exception as e:
            logger.error(f"Error updating conversation history: {str(e)}")
            pass

# Global agent instance
agent = None

def get_agent():
    """Get or create agent instance"""
    global agent
    if agent is None:
        agent = LightweightAIAgent()
    return agent

# Web Interface HTML (simplified for space)
WEB_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <title>Free AI Agent with LLM</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: system-ui, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 900px; margin: 0 auto; background: white; border-radius: 15px; box-shadow: 0 20px 40px rgba(0,0,0,0.1); overflow: hidden; }
        .header { background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%); color: white; padding: 30px; text-align: center; }
        .header h1 { margin: 0; font-size: 2.5em; font-weight: 300; }
        .header p { margin: 10px 0 0 0; opacity: 0.9; }
        .status { background: #27ae60; color: white; padding: 10px; text-align: center; font-weight: bold; }
        .chat-container { padding: 20px; }
        .chat-box { height: 400px; overflow-y: auto; padding: 20px; margin-bottom: 20px; background: #f8f9fa; border-radius: 10px; }
        .message { margin: 15px 0; padding: 15px 20px; border-radius: 20px; max-width: 80%; word-wrap: break-word; }
        .user { background: linear-gradient(135deg, #3498db, #2980b9); color: white; margin-left: auto; }
        .agent { background: white; border: 2px solid #ecf0f1; }
        .input-area { display: flex; gap: 15px; }
        input[type="text"] { flex: 1; padding: 15px 20px; border: 2px solid #e9ecef; border-radius: 25px; font-size: 16px; outline: none; }
        button { padding: 15px 30px; background: linear-gradient(135deg, #27ae60, #2ecc71); color: white; border: none; border-radius: 25px; cursor: pointer; font-size: 16px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Free AI Agent</h1>
            <p>Enhanced with Free LLM • Express Compatible</p>
        </div>
        <div class="status">✅ Online & Ready • Free LLM Enhanced • File Operations • Programming Help</div>
        <div class="chat-container">
            <div class="chat-box" id="chatBox"></div>
            <div class="input-area">
                <input type="text" id="userInput" placeholder="Ask me anything - I now have free LLM capabilities!" onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
    </div>

    <script>
        function addMessage(content, isUser) {
            const chatBox = document.getElementById('chatBox');
            const message = document.createElement('div');
            message.className = `message ${isUser ? 'user' : 'agent'}`;
            message.innerHTML = content.replace(/\n/g, '<br>');
            chatBox.appendChild(message);
            chatBox.scrollTop = chatBox.scrollHeight;
        }

        function handleKeyPress(event) {
            if (event.key === 'Enter') sendMessage();
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
                addMessage(data.result || data.error || 'No response received', false);
            } catch (error) {
                addMessage('❌ Connection error: ' + error.message, false);
            }
        }

        window.onload = function() {
            addMessage(`👋 **Welcome to Free AI Agent with LLM!**

I'm your enhanced AI assistant with **free Hugging Face LLM capabilities**! Now I can provide more natural, intelligent responses.

**🚀 Enhanced Features:**
• Free LLM integration for natural conversation
• Enhanced programming assistance
• Better understanding of complex queries
• File operations and general knowledge

Try asking me anything!`, false);
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
    """Handle chat requests - Compatible with Express application"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        session_id = data.get('session_id', 'default-session')
        context = data.get('context', None)
        
        if not message:
            return jsonify({"error": "No message provided"})
        
        # Get agent and process message
        current_agent = get_agent()
        result = current_agent.execute_task(message)
        
        # Format response to match Express application expectations
        response_data = {
            "result": result.get('result', ''),
            "text": result.get('result', ''),  # Alternative field name
            "status": result.get('status', 'completed'),
            "type": result.get('type', 'general'),
            "response_type": result.get('type', 'general'),
            "timestamp": time.time(),
            "execution_time": result.get('execution_time', 0),
            "agent_type": "Free AI Agent with LLM",
            "source": "ai_agent",
            "buttons": [],
            "showOptions": False,
            "session_id": session_id
        }
        
        # Add semantic analysis if available
        if 'semantic_analysis' in result:
            response_data['semantic_analysis'] = result['semantic_analysis']
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({
            "error": f"Server error: {str(e)}",
            "text": "Sorry, I encountered an error. Please try again.",
            "status": "error",
            "source": "error"
        })

@app.route('/health', methods=['GET'])
def health():
    """Health check for deployment - Compatible with Express middleware"""
    return jsonify({
        "status": "healthy",
        "version": "lightweight_llm",
        "timestamp": time.time(),
        "memory_optimized": True,
        "llm_available": HF_AVAILABLE and not get_agent().free_llm.fallback_mode,
        "features": {
            "file_operations": True,
            "programming_help": True,
            "general_knowledge": True,
            "free_llm": HF_AVAILABLE,
            "semantic_processing": True,
            "context_awareness": True
        }
    })

@app.route('/status', methods=['GET'])
def status():
    """Alternative status endpoint for Express compatibility"""
    return health()

@app.route('/execute-task', methods=['POST'])
def execute_task():
    """Execute AI task endpoint for Express compatibility"""
    try:
        data = request.get_json()
        task = data.get('task', '')
        priority = data.get('priority', 5)
        context = data.get('context', None)
        
        if not task:
            return jsonify({"error": "Task description is required"})
        
        # Get agent and execute task
        current_agent = get_agent()
        result = current_agent.execute_task(task)
        
        # Format response for Express compatibility
        response_data = {
            "task_id": f"task_{int(time.time())}",
            "status": result.get('status', 'completed'),
            "result": result.get('result', ''),
            "response": result.get('result', ''),  # Alternative field name
            "timestamp": time.time(),
            "execution_time": result.get('execution_time', 0),
            "type": result.get('type', 'general'),
            "priority": priority
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Task execution error: {e}")
        return jsonify({
            "error": f"Task execution failed: {str(e)}",
            "status": "failed"
        })

# Main function for deployment
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    
    if os.environ.get('PORT'):
        # Cloud deployment mode
        logger.info("🌐 Starting Free AI Agent with LLM for cloud deployment...")
        app.run(host='0.0.0.0', port=port)
    else:
        # Local development mode
        logger.info("🤖 Free AI Agent with Free LLM - Local Development Mode")
        logger.info(f"🌐 Web interface: http://localhost:{port}")
        app.run(host='localhost', port=port, debug=True)