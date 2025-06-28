#!/usr/bin/env python3
"""
Demonstration script for the Autonomous AI Agent
Shows basic functionality without requiring API keys
"""

import os
import sys
import json
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from autonomous_agent import MemoryManager, AgentTools, Task, TaskStatus, MemoryEntry


def demo_memory_system():
    """Demonstrate the memory management system"""
    print("🧠 Memory System Demonstration")
    print("-" * 40)
    
    # Initialize memory manager
    memory = MemoryManager("demo_memory.db")
    
    # Store some sample memories
    memories_to_store = [
        MemoryEntry(
            id="demo_1",
            type="long_term",
            content="Python is a versatile programming language excellent for AI development",
            context="programming_knowledge",
            timestamp=datetime.now(),
            importance=9
        ),
        MemoryEntry(
            id="demo_2", 
            type="short_term",
            content="Currently working on autonomous agent implementation",
            context="current_task",
            timestamp=datetime.now(),
            importance=7
        ),
        MemoryEntry(
            id="demo_3",
            type="long_term",
            content="LangChain is a framework for building LLM applications",
            context="technical_knowledge",
            timestamp=datetime.now(),
            importance=8
        )
    ]
    
    for memory_entry in memories_to_store:
        memory.store_memory(memory_entry)
        print(f"📝 Stored: {memory_entry.content[:50]}...")
    
    # Retrieve and display memories
    print("\n🔍 Retrieved Memories:")
    retrieved = memory.retrieve_memories(limit=5)
    for mem in retrieved:
        print(f"  • [{mem.type}] {mem.content}")
    
    # Store a sample task
    task = Task(
        id="demo_task_1",
        description="Demonstrate autonomous agent capabilities",
        status=TaskStatus.COMPLETED,
        priority=5,
        created_at=datetime.now(),
        result="Successfully demonstrated all core features"
    )
    memory.store_task(task)
    print(f"\n✅ Task stored: {task.description}")
    
    # Track some sample costs
    memory.track_cost("demo:gpt-4", 1500, 0.045, task.id)
    memory.track_cost("demo:llama3", 2000, 0.0, task.id)
    
    cost_summary = memory.get_cost_summary()
    print(f"\n💰 Cost Summary: {json.dumps(cost_summary, indent=2)}")
    
    return memory


def demo_agent_tools():
    """Demonstrate the agent tools functionality"""
    print("\n🔧 Agent Tools Demonstration")
    print("-" * 40)
    
    tools = AgentTools()
    
    # 1. Directory listing
    print("📁 Current Directory Contents:")
    dir_result = tools.list_directory(".")
    print(dir_result[:300] + "..." if len(dir_result) > 300 else dir_result)
    
    # 2. File operations
    print("\n📄 File Operations:")
    sample_content = """# Autonomous AI Agent Demo

This file was created by the autonomous agent's file writing capability.

## Features Demonstrated:
- Task decomposition and planning
- Tool usage (web search, file I/O, API calls)
- Memory management (short-term and long-term)
- Self-correction and retry logic
- Cost and token monitoring

## Technical Stack:
- Python 3.10+
- LangChain framework
- SQLite for persistence
- Support for OpenAI and Ollama models

Generated at: """ + datetime.now().isoformat()
    
    write_result = tools.write_file("demo_output.md", sample_content)
    print(f"Write result: {write_result}")
    
    read_result = tools.read_file("demo_output.md")
    print(f"Read result: {read_result[:200]}...")
    
    # 3. Web search (basic connectivity test)
    print("\n🌐 Web Search Capability:")
    search_result = tools.web_search("autonomous AI agents")
    print(f"Search result: {search_result[:300]}...")
    
    # 4. API call simulation
    print("\n🌍 API Call Capability:")
    api_result = tools.make_api_call("https://httpbin.org/get")
    print(f"API result: {api_result[:200]}...")


def demo_complete_workflow():
    """Demonstrate a complete autonomous workflow simulation"""
    print("\n🤖 Complete Workflow Simulation")
    print("-" * 40)
    
    # Initialize components
    memory = MemoryManager("workflow_demo.db")
    tools = AgentTools()
    
    # Simulate a complex task breakdown
    main_task = "Research Python AI frameworks and create a comparison report"
    
    print(f"📋 Main Task: {main_task}")
    
    # Simulate task decomposition
    subtasks = [
        "Research popular Python AI frameworks",
        "Compare features and capabilities", 
        "Analyze use cases and performance",
        "Create structured comparison report",
        "Save report to file"
    ]
    
    print("\n🔄 Task Decomposition:")
    for i, subtask in enumerate(subtasks, 1):
        print(f"  {i}. {subtask}")
    
    # Simulate executing subtasks
    print("\n⚡ Simulated Execution:")
    
    # Subtask 1: Research
    print("1. 🔍 Researching AI frameworks...")
    search_result = tools.web_search("Python AI frameworks comparison")
    memory_entry = MemoryEntry(
        id="research_1",
        type="short_term",
        content=f"Research findings: {search_result[:100]}...",
        context="task_execution",
        timestamp=datetime.now(),
        importance=7
    )
    memory.store_memory(memory_entry)
    
    # Subtask 2-4: Analysis and comparison (simulated)
    analysis_data = {
        "frameworks": ["TensorFlow", "PyTorch", "LangChain", "Scikit-learn"],
        "comparison_criteria": ["Ease of use", "Performance", "Community", "Documentation"],
        "findings": "Each framework has specific strengths for different AI applications"
    }
    
    print("2. 📊 Analyzing frameworks...")
    print("3. 🔍 Comparing capabilities...")
    print("4. 📋 Creating comparison report...")
    
    # Subtask 5: Save report
    report_content = f"""# Python AI Frameworks Comparison Report

Generated: {datetime.now().isoformat()}

## Frameworks Analyzed:
{chr(10).join([f"- {fw}" for fw in analysis_data['frameworks']])}

## Comparison Criteria:
{chr(10).join([f"- {criteria}" for criteria in analysis_data['comparison_criteria']])}

## Key Findings:
{analysis_data['findings']}

## Recommendations:
- TensorFlow: Best for production ML systems
- PyTorch: Excellent for research and experimentation  
- LangChain: Ideal for LLM applications
- Scikit-learn: Perfect for traditional ML tasks

## Conclusion:
The choice of framework depends on specific project requirements, 
team expertise, and deployment constraints.
"""
    
    print("5. 💾 Saving report...")
    write_result = tools.write_file("ai_frameworks_comparison.md", report_content)
    print(f"   {write_result}")
    
    # Store task completion in memory
    completion_entry = MemoryEntry(
        id="task_complete",
        type="long_term", 
        content=f"Successfully completed: {main_task}",
        context="task_completion",
        timestamp=datetime.now(),
        importance=9
    )
    memory.store_memory(completion_entry)
    
    print("\n✅ Workflow completed successfully!")
    print(f"📄 Report saved to: ai_frameworks_comparison.md")
    
    # Show memory state
    print("\n🧠 Final Memory State:")
    memories = memory.retrieve_memories(limit=3)
    for mem in memories:
        print(f"  • [{mem.type}] {mem.content[:60]}...")


def main():
    """Run the complete demonstration"""
    print("🚀 Autonomous AI Agent - Complete Demonstration")
    print("=" * 60)
    print("This demo shows all capabilities without requiring API keys")
    print("=" * 60)
    
    try:
        # Run all demonstrations
        demo_memory_system()
        demo_agent_tools()
        demo_complete_workflow()
        
        print("\n🎉 Demonstration completed successfully!")
        print("\n📝 Files created during demo:")
        print("  • demo_output.md - Sample agent-generated content")
        print("  • ai_frameworks_comparison.md - Complete analysis report")
        print("  • demo_memory.db - Memory system database")
        print("  • workflow_demo.db - Workflow demonstration database")
        
        print("\n🔧 To use with real AI models:")
        print("  1. Set OPENAI_API_KEY in .env file for OpenAI models")
        print("  2. Install and run Ollama for local models")
        print("  3. Run: python autonomous_agent.py")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up demo databases (optional)
        for db_file in ["demo_memory.db", "workflow_demo.db"]:
            if os.path.exists(db_file) and input(f"\nDelete {db_file}? (y/N): ").lower() == 'y':
                os.remove(db_file)
                print(f"🗑️ Deleted {db_file}")


if __name__ == "__main__":
    main()