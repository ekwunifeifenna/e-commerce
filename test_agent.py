#!/usr/bin/env python3
"""
Test script for the Autonomous AI Agent
"""

import os
import sys
import json
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autonomous_agent import AutonomousAgent, MemoryManager, AgentTools


def test_memory_manager():
    """Test the memory manager functionality"""
    print("🧠 Testing Memory Manager...")
    
    # Initialize memory manager
    memory = MemoryManager("test_memory.db")
    
    # Test storing and retrieving memories
    from autonomous_agent import MemoryEntry
    
    entry = MemoryEntry(
        id="test_1",
        type="short_term",
        content="Test memory content",
        context="testing",
        timestamp=datetime.now(),
        importance=5
    )
    
    memory.store_memory(entry)
    memories = memory.retrieve_memories(limit=1)
    
    assert len(memories) == 1
    assert memories[0].content == "Test memory content"
    print("✅ Memory Manager test passed")


def test_agent_tools():
    """Test the agent tools"""
    print("🔧 Testing Agent Tools...")
    
    tools = AgentTools()
    
    # Test directory listing
    result = tools.list_directory(".")
    assert "autonomous_agent.py" in result
    print("✅ Directory listing works")
    
    # Test file operations
    test_content = "Hello, test file!"
    tools.write_file("test_file.txt", test_content)
    
    read_result = tools.read_file("test_file.txt")
    assert test_content in read_result
    print("✅ File operations work")
    
    # Clean up
    os.remove("test_file.txt")
    
    # Test web search (basic connectivity)
    search_result = tools.web_search("Python programming")
    assert len(search_result) > 0
    print("✅ Web search works")


def test_agent_initialization():
    """Test agent initialization with fallback"""
    print("🤖 Testing Agent Initialization...")
    
    try:
        # Try OpenAI first
        agent = AutonomousAgent(model_type="openai", model_name="gpt-4")
        print("✅ OpenAI agent initialized successfully")
        return agent
    except Exception as e:
        print(f"⚠️ OpenAI failed ({e}), trying Ollama...")
        
        try:
            agent = AutonomousAgent(model_type="ollama", model_name="llama3")
            print("✅ Ollama agent initialized successfully")
            return agent
        except Exception as e:
            print(f"❌ Both OpenAI and Ollama failed: {e}")
            return None


def test_simple_task(agent):
    """Test a simple task execution"""
    if not agent:
        print("❌ Cannot test task execution - no agent available")
        return
    
    print("📋 Testing Simple Task Execution...")
    
    # Test a simple file operation task
    result = agent.execute_task(
        "List the files in the current directory and create a summary",
        priority=3
    )
    
    print(f"Task Status: {result['status']}")
    print(f"Attempts: {result['attempts']}")
    
    if result['status'] == 'completed':
        print("✅ Simple task execution passed")
        print(f"Result preview: {result['result'][:200]}...")
    else:
        print(f"⚠️ Task failed: {result.get('error', 'Unknown error')}")


def test_agent_status(agent):
    """Test agent status reporting"""
    if not agent:
        print("❌ Cannot test status - no agent available")
        return
    
    print("📊 Testing Agent Status...")
    
    status = agent.get_status()
    
    print("Agent Status:")
    print(f"- Model: {status['agent_info']['model_type']}:{status['agent_info']['model_name']}")
    print(f"- Memory entries: {status['memory_entries']}")
    print(f"- Task statistics: {status['task_statistics']}")
    
    print("✅ Status reporting works")


def main():
    """Run all tests"""
    print("🚀 Starting Autonomous AI Agent Tests")
    print("=" * 50)
    
    # Run tests
    try:
        test_memory_manager()
        test_agent_tools()
        agent = test_agent_initialization()
        test_simple_task(agent)
        test_agent_status(agent)
        
        print("\n🎉 All tests completed!")
        
        # Clean up test database
        if os.path.exists("test_memory.db"):
            os.remove("test_memory.db")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()