"""
Simple Autonomous AI Agent

Core functionality: Execute tasks using LangChain with basic file operations
"""

import os
import logging
from typing import Dict, Any

# LangChain imports
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FileOperations:
    """File operation tools for the agent"""
    
    @staticmethod
    def read_file(file_path: str) -> str:
        """Read content from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return f"File content:\n{content}"
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    @staticmethod
    def write_file(file_path: str, content: str) -> str:
        """Write content to a file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    @staticmethod
    def list_directory(path: str) -> str:
        """List contents of a directory"""
        try:
            items = os.listdir(path)
            return f"Directory contents: {', '.join(items)}"
        except Exception as e:
            return f"Error listing directory: {str(e)}"


class SimpleAgent:
    """Core autonomous agent"""
    
    def __init__(self):
        # Initialize OpenAI model
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found")
        
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.1)
        
        # Initialize tools
        file_ops = FileOperations()
        self.tools = [
            Tool(
                name="read_file",
                description="Read file content. Input: file path",
                func=file_ops.read_file
            ),
            Tool(
                name="write_file", 
                description="Write to file. Input: 'filepath|content'",
                func=lambda x: file_ops.write_file(*x.split('|', 1)) if '|' in x else "Invalid format"
            ),
            Tool(
                name="list_directory",
                description="List directory contents. Input: directory path", 
                func=file_ops.list_directory
            )
        ]
        
        # Create agent prompt
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""You are an AI agent with file operation tools.
            Available tools: read_file, write_file, list_directory.
            Use tools to complete tasks and provide clear responses."""),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessage(content="{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
        
        # Create memory and agent
        self.memory = ConversationBufferWindowMemory(
            memory_key="chat_history", 
            return_messages=True, 
            k=5
        )
        
        agent = create_openai_tools_agent(self.llm, self.tools, prompt)
        self.executor = AgentExecutor(
            agent=agent, 
            tools=self.tools, 
            memory=self.memory,
            verbose=True
        )
    
    def execute_task(self, task: str) -> Dict[str, Any]:
        """Execute a task and return result"""
        try:
            result = self.executor.invoke({"input": task})
            return {"status": "completed", "result": result.get('output')}
        except Exception as e:
            return {"status": "failed", "error": str(e)}


def main():
    """Demo the agent"""
    print("🤖 Simple AI Agent Demo")
    
    try:
        agent = SimpleAgent()
        print("✅ Agent initialized")
        
        # Demo task
        result = agent.execute_task("Create a file called 'test.txt' with content 'Hello World!'")
        print(f"Task result: {result}")
        
        # Interactive mode
        print("\nChat mode (type 'exit' to quit):")
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == 'exit':
                break
            if user_input:
                result = agent.execute_task(user_input)
                print(f"Agent: {result.get('result', result.get('error'))}")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()