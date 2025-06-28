"""
Autonomous AI Agent with Planning, Execution, and Self-Correction Capabilities

This module implements a comprehensive autonomous agent that can:
- Decompose complex tasks into subtasks
- Use various tools (web search, file I/O, API calls)
- Maintain short and long-term memory
- Self-correct failed actions
- Monitor costs and token usage
"""

import os
import json
import sqlite3
import logging
import time
from datetime import datetime
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

# LangChain imports
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory

# External dependencies
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TaskStatus(Enum):
    """Enum for task status tracking"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"


@dataclass
class Task:
    """Data class representing a task"""
    id: str
    description: str
    status: TaskStatus
    priority: int
    created_at: datetime
    subtasks: List[str] = None
    attempts: int = 0
    max_attempts: int = 3
    result: Optional[str] = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.subtasks is None:
            self.subtasks = []


@dataclass
class MemoryEntry:
    """Data class for memory entries"""
    id: str
    type: str  # 'short_term' or 'long_term'
    content: str
    context: str
    timestamp: datetime
    importance: int  # 1-10 scale


class MemoryManager:
    """Manages short-term and long-term memory using SQLite"""
    
    def __init__(self, db_path: str = "agent_memory.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize the SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create memory table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memory (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    context TEXT,
                    timestamp TEXT NOT NULL,
                    importance INTEGER DEFAULT 5
                )
            """)
            
            # Create tasks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL,
                    priority INTEGER DEFAULT 5,
                    created_at TEXT NOT NULL,
                    subtasks TEXT,
                    attempts INTEGER DEFAULT 0,
                    max_attempts INTEGER DEFAULT 3,
                    result TEXT,
                    error TEXT
                )
            """)
            
            # Create cost tracking table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cost_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    model TEXT NOT NULL,
                    tokens_used INTEGER,
                    estimated_cost REAL,
                    task_id TEXT
                )
            """)
            
            conn.commit()
    
    def store_memory(self, entry: MemoryEntry):
        """Store a memory entry"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO memory 
                (id, type, content, context, timestamp, importance)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                entry.id, entry.type, entry.content, entry.context,
                entry.timestamp.isoformat(), entry.importance
            ))
            conn.commit()
    
    def retrieve_memories(self, memory_type: str = None, limit: int = 10) -> List[MemoryEntry]:
        """Retrieve memories by type"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if memory_type:
                cursor.execute("""
                    SELECT * FROM memory 
                    WHERE type = ? 
                    ORDER BY timestamp DESC, importance DESC 
                    LIMIT ?
                """, (memory_type, limit))
            else:
                cursor.execute("""
                    SELECT * FROM memory 
                    ORDER BY timestamp DESC, importance DESC 
                    LIMIT ?
                """, (limit,))
            
            rows = cursor.fetchall()
            return [
                MemoryEntry(
                    id=row[0], type=row[1], content=row[2], context=row[3],
                    timestamp=datetime.fromisoformat(row[4]), importance=row[5]
                )
                for row in rows
            ]
    
    def store_task(self, task: Task):
        """Store a task"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO tasks 
                (id, description, status, priority, created_at, subtasks, 
                 attempts, max_attempts, result, error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task.id, task.description, task.status.value, task.priority,
                task.created_at.isoformat(), json.dumps(task.subtasks),
                task.attempts, task.max_attempts, task.result, task.error
            ))
            conn.commit()
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            
            if row:
                return Task(
                    id=row[0], description=row[1], 
                    status=TaskStatus(row[2]), priority=row[3],
                    created_at=datetime.fromisoformat(row[4]),
                    subtasks=json.loads(row[5]) if row[5] else [],
                    attempts=row[6], max_attempts=row[7],
                    result=row[8], error=row[9]
                )
            return None
    
    def track_cost(self, model: str, tokens_used: int, estimated_cost: float, task_id: str = None):
        """Track cost and token usage"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cost_tracking 
                (timestamp, model, tokens_used, estimated_cost, task_id)
                VALUES (?, ?, ?, ?, ?)
            """, (datetime.now().isoformat(), model, tokens_used, estimated_cost, task_id))
            conn.commit()
    
    def get_cost_summary(self) -> Dict[str, Any]:
        """Get cost summary"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    model,
                    SUM(tokens_used) as total_tokens,
                    SUM(estimated_cost) as total_cost,
                    COUNT(*) as total_calls
                FROM cost_tracking 
                GROUP BY model
            """)
            
            summary = {}
            for row in cursor.fetchall():
                summary[row[0]] = {
                    'total_tokens': row[1],
                    'total_cost': row[2],
                    'total_calls': row[3]
                }
            
            return summary


class AgentTools:
    """Collection of tools for the autonomous agent"""
    
    @staticmethod
    def web_search(query: str) -> str:
        """Perform web search using a simple API"""
        try:
            # Using DuckDuckGo instant answer API (no API key required)
            url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract relevant information
            result = []
            if data.get('Abstract'):
                result.append(f"Abstract: {data['Abstract']}")
            if data.get('Answer'):
                result.append(f"Answer: {data['Answer']}")
            if data.get('RelatedTopics'):
                topics = [topic.get('Text', '') for topic in data['RelatedTopics'][:3]]
                result.append(f"Related: {'; '.join(topics)}")
            
            return '\n'.join(result) if result else f"No detailed results found for: {query}"
            
        except Exception as e:
            logger.error(f"Web search failed: {e}")
            return f"Web search failed: {str(e)}"
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """Read content from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return f"File content ({len(content)} characters):\n{content}"
        except Exception as e:
            logger.error(f"Failed to read file {file_path}: {e}")
            return f"Error reading file: {str(e)}"
    
    @staticmethod
    def write_file(file_path: str, content: str) -> str:
        """Write content to a file"""
        try:
            # Ensure the file path is not empty and handle directory creation properly
            if not file_path:
                return "Error: file_path cannot be empty"
            
            # Create directory if it doesn't exist
            dir_path = os.path.dirname(file_path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return f"Successfully wrote {len(content)} characters to {file_path}"
        except Exception as e:
            logger.error(f"Failed to write file {file_path}: {e}")
            return f"Error writing file: {str(e)}"
    
    @staticmethod
    def make_api_call(url: str, method: str = "GET", headers: Dict = None, data: Dict = None) -> str:
        """Make an API call"""
        try:
            headers = headers or {}
            method = method.upper()
            
            if method == "GET":
                response = requests.get(url, headers=headers, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data, timeout=10)
            elif method == "PUT":
                response = requests.put(url, headers=headers, json=data, timeout=10)
            else:
                return f"Unsupported HTTP method: {method}"
            
            response.raise_for_status()
            
            try:
                return f"API Response ({response.status_code}):\n{response.json()}"
            except:
                return f"API Response ({response.status_code}):\n{response.text}"
                
        except Exception as e:
            logger.error(f"API call failed: {e}")
            return f"API call failed: {str(e)}"
    
    @staticmethod
    def list_directory(path: str) -> str:
        """List contents of a directory"""
        try:
            if not os.path.exists(path):
                return f"Directory does not exist: {path}"
            
            items = []
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    items.append(f"📁 {item}/")
                else:
                    size = os.path.getsize(item_path)
                    items.append(f"📄 {item} ({size} bytes)")
            
            return f"Directory contents of {path}:\n" + "\n".join(items)
            
        except Exception as e:
            logger.error(f"Failed to list directory {path}: {e}")
            return f"Error listing directory: {str(e)}"


class AutonomousAgent:
    """Main autonomous agent class with planning, execution, and self-correction"""
    
    def __init__(self, model_type: str = "openai", model_name: str = "gpt-4"):
        self.model_type = model_type
        self.model_name = model_name
        self.memory = MemoryManager()
        self.current_task_id = None
        
        # Initialize the language model
        self._init_llm()
        
        # Initialize tools
        self._init_tools()
        
        # Initialize agent
        self._init_agent()
        
        logger.info(f"Autonomous Agent initialized with {model_type} model: {model_name}")
    
    def _init_llm(self):
        """Initialize the language model"""
        if self.model_type.lower() == "openai":
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OPENAI_API_KEY not found in environment variables")
            
            self.llm = ChatOpenAI(
                model=self.model_name,
                temperature=0.1,
                openai_api_key=api_key
            )
        elif self.model_type.lower() == "ollama":
            self.llm = Ollama(
                model=self.model_name,
                base_url=os.getenv('OLLAMA_HOST', 'http://localhost:11434')
            )
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")
    
    def _init_tools(self):
        """Initialize agent tools"""
        tools = AgentTools()
        
        self.tools = [
            Tool(
                name="web_search",
                description="Search the web for information. Input should be a search query string.",
                func=tools.web_search
            ),
            Tool(
                name="read_file",
                description="Read content from a file. Input should be the file path.",
                func=tools.read_file
            ),
            Tool(
                name="write_file",
                description="Write content to a file. Input should be 'file_path|content' separated by |",
                func=lambda x: tools.write_file(*x.split('|', 1)) if '|' in x else "Invalid format. Use: file_path|content"
            ),
            Tool(
                name="api_call",
                description="Make an API call. Input should be JSON with url, method, headers, data fields.",
                func=lambda x: tools.make_api_call(**json.loads(x))
            ),
            Tool(
                name="list_directory",
                description="List contents of a directory. Input should be the directory path.",
                func=tools.list_directory
            )
        ]
    
    def _init_agent(self):
        """Initialize the LangChain agent"""
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=self._get_system_prompt()),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessage(content="{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # Create memory
        self.agent_memory = ConversationBufferWindowMemory(
            memory_key="chat_history",
            return_messages=True,
            k=10  # Keep last 10 exchanges
        )
        
        # Create the agent
        if self.model_type.lower() == "openai":
            self.agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        else:
            # For Ollama, we'll use a simpler approach
            from langchain.agents import create_react_agent
            self.agent = create_react_agent(self.llm, self.tools, prompt)
        
        # Create executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            memory=self.agent_memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=10
        )
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the agent"""
        return """You are an autonomous AI agent with advanced planning, execution, and self-correction capabilities.

Your core abilities:
1. TASK DECOMPOSITION: Break complex goals into manageable subtasks
2. TOOL USAGE: Use available tools for web search, file operations, API calls
3. MEMORY MANAGEMENT: Store and retrieve relevant information
4. SELF-CORRECTION: Identify failures and retry with different approaches
5. COST AWARENESS: Monitor token usage and costs

Available tools:
- web_search: Search the web for information
- read_file: Read file contents
- write_file: Write content to files (format: file_path|content)
- api_call: Make HTTP API calls (JSON format)
- list_directory: List directory contents

Guidelines:
- Always decompose complex tasks into smaller, manageable subtasks
- Use tools strategically to gather information before acting
- If a task fails, analyze the failure and try a different approach
- Store important information in memory for future reference
- Be thorough but efficient in your approach
- Always provide clear explanations of your reasoning

When given a task:
1. Analyze and break it down into subtasks
2. Plan your approach step by step
3. Execute using available tools
4. Monitor progress and adjust as needed
5. Self-correct if something goes wrong
6. Provide a comprehensive summary

Remember: You are autonomous - make decisions and take actions to complete tasks successfully."""

    def execute_task(self, task_description: str, priority: int = 5) -> Dict[str, Any]:
        """Execute a task with full autonomous capabilities"""
        # Create task
        task_id = f"task_{int(time.time())}"
        task = Task(
            id=task_id,
            description=task_description,
            status=TaskStatus.PENDING,
            priority=priority,
            created_at=datetime.now()
        )
        
        self.current_task_id = task_id
        self.memory.store_task(task)
        
        logger.info(f"Starting task execution: {task_description}")
        
        # Store task in short-term memory
        memory_entry = MemoryEntry(
            id=f"task_start_{task_id}",
            type="short_term",
            content=f"Started task: {task_description}",
            context="task_execution",
            timestamp=datetime.now(),
            importance=priority
        )
        self.memory.store_memory(memory_entry)
        
        try:
            # Update task status
            task.status = TaskStatus.IN_PROGRESS
            task.attempts += 1
            self.memory.store_task(task)
            
            # Execute the task
            result = self._execute_with_retry(task)
            
            # Update task with result
            task.status = TaskStatus.COMPLETED
            task.result = result.get('output', '')
            self.memory.store_task(task)
            
            # Store successful completion in memory
            memory_entry = MemoryEntry(
                id=f"task_complete_{task_id}",
                type="long_term",
                content=f"Completed task: {task_description}. Result: {task.result[:200]}...",
                context="task_completion",
                timestamp=datetime.now(),
                importance=min(priority + 2, 10)
            )
            self.memory.store_memory(memory_entry)
            
            logger.info(f"Task completed successfully: {task_id}")
            return {
                'task_id': task_id,
                'status': 'completed',
                'result': task.result,
                'attempts': task.attempts
            }
            
        except Exception as e:
            # Handle failure
            task.status = TaskStatus.FAILED
            task.error = str(e)
            self.memory.store_task(task)
            
            logger.error(f"Task failed: {task_id}, Error: {e}")
            
            # Store failure in memory for learning
            memory_entry = MemoryEntry(
                id=f"task_failed_{task_id}",
                type="long_term",
                content=f"Failed task: {task_description}. Error: {str(e)}",
                context="task_failure",
                timestamp=datetime.now(),
                importance=8
            )
            self.memory.store_memory(memory_entry)
            
            return {
                'task_id': task_id,
                'status': 'failed',
                'error': str(e),
                'attempts': task.attempts
            }
    
    def _execute_with_retry(self, task: Task) -> Dict[str, Any]:
        """Execute task with retry logic"""
        max_attempts = task.max_attempts
        
        for attempt in range(max_attempts):
            try:
                # Get relevant memories
                memories = self.memory.retrieve_memories(limit=5)
                memory_context = "\n".join([f"- {m.content}" for m in memories])
                
                # Prepare enhanced input with context
                enhanced_input = f"""
TASK: {task.description}
ATTEMPT: {attempt + 1}/{max_attempts}

RELEVANT MEMORY CONTEXT:
{memory_context}

Please execute this task step by step. If this is a retry, consider what might have gone wrong before and try a different approach.
"""
                
                # Track token usage (estimated)
                start_time = time.time()
                
                # Execute using the agent
                result = self.agent_executor.invoke({
                    "input": enhanced_input
                })
                
                execution_time = time.time() - start_time
                
                # Estimate cost (rough approximation)
                estimated_tokens = len(enhanced_input.split()) * 1.3 + len(str(result).split()) * 1.3
                estimated_cost = self._estimate_cost(estimated_tokens)
                
                # Track cost
                self.memory.track_cost(
                    model=f"{self.model_type}:{self.model_name}",
                    tokens_used=int(estimated_tokens),
                    estimated_cost=estimated_cost,
                    task_id=task.id
                )
                
                logger.info(f"Task execution completed in {execution_time:.2f}s, estimated {int(estimated_tokens)} tokens")
                
                return result
                
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                
                if attempt < max_attempts - 1:
                    # Store retry attempt in memory
                    memory_entry = MemoryEntry(
                        id=f"retry_{task.id}_{attempt}",
                        type="short_term",
                        content=f"Retry attempt {attempt + 1} for task {task.description}. Error: {str(e)}",
                        context="task_retry",
                        timestamp=datetime.now(),
                        importance=6
                    )
                    self.memory.store_memory(memory_entry)
                    
                    # Update task status
                    task.status = TaskStatus.RETRYING
                    task.attempts = attempt + 1
                    task.error = str(e)
                    self.memory.store_task(task)
                    
                    # Wait before retry
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise e
    
    def _estimate_cost(self, tokens: int) -> float:
        """Estimate cost based on model and tokens"""
        # Cost estimates (per 1K tokens)
        cost_per_1k = {
            'openai:gpt-4': 0.03,
            'openai:gpt-3.5-turbo': 0.002,
            'ollama': 0.0  # Local models are free
        }
        
        model_key = f"{self.model_type}:{self.model_name}"
        rate = cost_per_1k.get(model_key, 0.01)  # Default rate
        
        return (tokens / 1000) * rate
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status and statistics"""
        cost_summary = self.memory.get_cost_summary()
        
        # Get recent tasks
        with sqlite3.connect(self.memory.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM tasks 
                GROUP BY status
            """)
            task_stats = dict(cursor.fetchall())
        
        return {
            'agent_info': {
                'model_type': self.model_type,
                'model_name': self.model_name,
                'current_task': self.current_task_id
            },
            'cost_summary': cost_summary,
            'task_statistics': task_stats,
            'memory_entries': len(self.memory.retrieve_memories(limit=1000))
        }
    
    def chat(self, message: str) -> str:
        """Simple chat interface"""
        try:
            result = self.agent_executor.invoke({"input": message})
            return result.get('output', 'No response generated')
        except Exception as e:
            logger.error(f"Chat failed: {e}")
            return f"Sorry, I encountered an error: {str(e)}"


def main():
    """Main function to demonstrate the autonomous agent"""
    print("🤖 Autonomous AI Agent - Demonstration")
    print("=" * 50)
    
    try:
        # Initialize agent (try OpenAI first, fallback to Ollama)
        try:
            agent = AutonomousAgent(model_type="openai", model_name="gpt-4")
            print("✅ Agent initialized with OpenAI GPT-4")
        except Exception as e:
            print(f"❌ OpenAI initialization failed: {e}")
            print("🔄 Falling back to Ollama...")
            agent = AutonomousAgent(model_type="ollama", model_name="llama3")
            print("✅ Agent initialized with Ollama Llama3")
        
        # Demonstrate capabilities
        print("\n🎯 Testing Agent Capabilities:")
        
        # 1. Simple task
        print("\n1. Simple Information Gathering Task:")
        result = agent.execute_task("Search for information about Python 3.12 new features")
        print(f"Status: {result['status']}")
        if result['status'] == 'completed':
            print(f"Result preview: {result['result'][:200]}...")
        
        # 2. File operation task
        print("\n2. File Operation Task:")
        result = agent.execute_task("Create a simple Python script that prints 'Hello, Autonomous World!' and save it as hello_agent.py")
        print(f"Status: {result['status']}")
        
        # 3. Get agent status
        print("\n📊 Agent Status:")
        status = agent.get_status()
        print(json.dumps(status, indent=2, default=str))
        
        # 4. Interactive chat
        print("\n💬 Interactive Chat Mode:")
        print("Type 'exit' to quit, 'status' for agent status")
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'exit':
                break
            elif user_input.lower() == 'status':
                status = agent.get_status()
                print("Agent Status:", json.dumps(status, indent=2, default=str))
            elif user_input:
                response = agent.chat(user_input)
                print(f"Agent: {response}")
        
        print("\n👋 Thanks for using the Autonomous AI Agent!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Main execution failed: {e}")


if __name__ == "__main__":
    main()