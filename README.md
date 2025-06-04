# ADK Crash Course

This repository contains various examples of agents built using the ADK (Agent Development Kit) framework. Each example demonstrates different capabilities and features of the framework.

## Setup Instructions

1. Install uv (Python package installer):
   - For detailed installation instructions, visit the [official uv documentation](https://docs.astral.sh/uv/getting-started/installation/)
   - Quick install (Unix/macOS):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   - Quick install (Windows PowerShell):
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
uv pip install -r requirements.txt
```

## Running the Agents

### Using ADK Web (Agents 1-4)
For the first four agents (Basic Agent, Tool Agent, LiteLLM Agent, and Structured Outputs), you can use ADK Web:

1. Start ADK Web:
```bash
adk web
```

2. Open your browser and navigate to `http://localhost:3000`

3. Select the agent you want to run from the available agents list:
   - Greeting Agent
   - Tool Agent
   - Dad Joke Agent
   - Email Agent

### Using Python (Agents 5-6)
For the Sessions and State (5) and Persistent Storage (6) agents, run them directly using Python:

1. For Question Answering Agent:
```bash
cd 5-sessions-and-state/question_answering_agent
python main.py
```

2. For Pizza Order Agent:
```bash
cd 6-persistent-storage/pizza_order_agent
python main.py
```

## Available Agents

### 1. Basic Agent
- **Greeting Agent**: A simple agent that greets users and asks for their name.
- Location: `1-basic-agent/greeting_agent/`
- Run using: ADK Web

### 2. Tool Agent
- **Tool Agent**: Demonstrates the use of tools with a simple time-telling functionality.
- Location: `2-tool-agent/tool-agent/`
- Run using: ADK Web

### 3. LiteLLM Agent
- **Dad Joke Agent**: An agent that generates dad jokes using the LiteLLM integration.
- Location: `3-litellm-agent/dad_joke_agent/`
- Run using: ADK Web

### 4. Structured Outputs
- **Email Agent**: Generates professional emails with structured subject and body using Pydantic models.
- Location: `4-structured-outputs/email_agent/`
- Run using: ADK Web

### 5. Sessions and State
- **Question Answering Agent**: Demonstrates stateful interactions and session management.
- Location: `5-sessions-and-state/question_answering_agent/`
- Run using: `python basic_stateful_session.py`

### 6. Persistent Storage
- **Pizza Order Agent**: A comprehensive example of an agent that manages pizza orders with persistent state, including:
  - Menu display
  - Pizza type and size selection
  - Toppings management
  - Quantity selection
  - Delivery information collection
  - Price calculation
- Location: `6-persistent-storage/pizza_order_agent/`
- Run using: `python main.py`

## Requirements

- Python 3.8+
- uv package manager
- Required environment variables (if applicable):
  - OPENROUTER_API_KEY (for LiteLLM agent)

## Contributing

Feel free to contribute to this project by submitting pull requests or opening issues for bugs and feature requests.
