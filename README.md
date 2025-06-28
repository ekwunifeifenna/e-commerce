# Autonomous AI Agent Implementation

## Overview
A comprehensive autonomous AI agent built with Python 3.10+ and LangChain that can plan, execute, and self-correct tasks with advanced capabilities including task decomposition, tool usage, memory management, and cost monitoring.

## Features
- **Task Decomposition**: Breaks complex goals into manageable subtasks
- **Tool Usage**: Web search, file I/O, API calls, directory operations
- **Memory Management**: Short-term and long-term memory with SQLite persistence
- **Self-Correction**: Automatic retry logic with exponential backoff
- **Cost Monitoring**: Token usage and cost tracking for different models
- **Multi-Model Support**: OpenAI GPT-4 and Ollama Llama 3

## Setup Instructions

### Step 1: Environment Setup
```bash
# Create virtual environment
python3.10 -m venv autonomous_agent_env
source autonomous_agent_env/bin/activate  # Linux/Mac
# autonomous_agent_env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configuration
1. Copy `.env` file and update with your API keys:
   ```bash
   cp .env .env.local
   # Edit .env.local with your actual API keys
   ```

2. For OpenAI (recommended):
   - Get API key from https://platform.openai.com/api-keys
   - Set `OPENAI_API_KEY=your_actual_key`

3. For Ollama (free alternative):
   ```bash
   # Install Ollama
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Pull Llama 3 model
   ollama pull llama3
   
   # Start Ollama server
   ollama serve
   ```

### Step 3: Basic Usage

#### Quick Start
```python
from autonomous_agent import AutonomousAgent

# Initialize with OpenAI
agent = AutonomousAgent(model_type="openai", model_name="gpt-4")

# OR initialize with Ollama
agent = AutonomousAgent(model_type="ollama", model_name="llama3")

# Execute a task
result = agent.execute_task("Research and summarize the latest AI developments")
print(f"Status: {result['status']}")
print(f"Result: {result['result']}")
```

#### Interactive Mode
```bash
python autonomous_agent.py
```

## Architecture

### Core Components

1. **AutonomousAgent**: Main orchestrator class
2. **MemoryManager**: SQLite-based persistence for tasks and memories
3. **AgentTools**: Collection of tools (web search, file ops, API calls)
4. **Task**: Data structure for task tracking and status
5. **MemoryEntry**: Short/long-term memory entries with importance scoring

### Database Schema
- **memory**: Stores agent memories with importance and context
- **tasks**: Tracks task execution, status, and results
- **cost_tracking**: Monitors token usage and estimated costs

## Advanced Usage

### Custom Task Execution
```python
# High priority complex task
result = agent.execute_task(
    "Analyze market trends, create a report, and save to analysis.md",
    priority=8
)

# Check agent status
status = agent.get_status()
print(f"Total cost: ${sum(model['total_cost'] for model in status['cost_summary'].values())}")
```

### Memory Management
```python
# Retrieve recent memories
memories = agent.memory.retrieve_memories(memory_type="long_term", limit=10)
for memory in memories:
    print(f"{memory.timestamp}: {memory.content}")
```

### Cost Monitoring
```python
# Get detailed cost breakdown
cost_summary = agent.memory.get_cost_summary()
for model, stats in cost_summary.items():
    print(f"{model}: {stats['total_tokens']} tokens, ${stats['total_cost']:.4f}")
```

## Tool Capabilities

1. **web_search**: DuckDuckGo API integration (no API key required)
2. **read_file/write_file**: Local file system operations
3. **api_call**: HTTP requests with full REST support
4. **list_directory**: File system exploration

## Error Handling & Self-Correction

The agent implements sophisticated error handling:
- **Exponential backoff** for retries (2^attempt seconds)
- **Memory-based learning** from previous failures
- **Context-aware retry strategies** using stored memories
- **Maximum attempt limits** to prevent infinite loops

## Performance Optimization

### Token Management
- Estimated token counting for cost tracking
- Memory context limited to most relevant entries
- Conversation buffer with sliding window (10 exchanges)

### Memory Efficiency
- SQLite with indexed queries for fast retrieval
- Importance-based memory prioritization
- Automatic cleanup of low-importance short-term memories

## Troubleshooting

### Common Issues

1. **OpenAI API Key Error**:
   ```
   ValueError: OPENAI_API_KEY not found in environment variables
   ```
   **Solution**: Set your API key in `.env` file

2. **Ollama Connection Error**:
   ```
   ConnectionError: Could not connect to Ollama
   ```
   **Solution**: Start Ollama server with `ollama serve`

3. **Import Errors**:
   **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

### Debug Mode
```python
import logging
logging.getLogger().setLevel(logging.DEBUG)

agent = AutonomousAgent(model_type="openai", model_name="gpt-4")
```

## Example Use Cases

### 1. Research Assistant
```python
result = agent.execute_task(
    "Research recent developments in quantum computing, "
    "summarize key breakthroughs, and create a markdown report"
)
```

### 2. Data Analysis
```python
result = agent.execute_task(
    "Read data.csv, analyze trends, create visualizations, "
    "and generate insights report"
)
```

### 3. API Integration
```python
result = agent.execute_task(
    "Fetch weather data from OpenWeatherMap API for New York, "
    "format the results, and save to weather_report.json"
)
```

### 4. File Management
```python
result = agent.execute_task(
    "Organize files in the downloads folder by type, "
    "create directories for each file type, and move files accordingly"
)
```

## Security Considerations

- **API Key Protection**: Use environment variables, never hardcode
- **File System Access**: Agent has read/write access to local file system
- **Web Requests**: All external requests are logged and rate-limited
- **Input Validation**: All tool inputs are validated before execution

## Limitations

1. **Local Environment**: Agent operates within local system constraints
2. **Model Dependencies**: Requires either OpenAI API access or local Ollama installation
3. **Internet Access**: Web search and API calls require internet connectivity
4. **Resource Usage**: Large tasks may consume significant tokens/compute

## Contributing

To extend the agent:

1. **Add New Tools**: Implement in `AgentTools` class
2. **Custom Memory Types**: Extend `MemoryManager` 
3. **Additional Models**: Add support in `_init_llm()` method
4. **Enhanced Planning**: Modify system prompt for better task decomposition

## License
See LICENSE file for details.