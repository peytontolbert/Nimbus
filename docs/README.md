# Documentation

This folder contains detailed documentation for the project. Below is a brief overview of the project structure and the purpose of each module.

## Project Structure

- **DETAILED_DOCUMENTATION.md**: Contains detailed documentation about the project.
- **PROJECT_STRUCTURE.md**: Provides an overview of the project structure.
- **agent/**: Contains the main agent code, including task management and message handling.
- **agent_data/**: Stores data related to the agent's operations, such as episodic and semantic memory.
- **data/**: Placeholder for data files used by the project.
- **gpt/**: Contains code related to GPT models, including chat and server functionalities.
- **interfaces/**: Defines various interfaces, such as HTTP server and user interface.
- **llm/**: Contains code for large language models, including entity extraction, task planning, reasoning, and summarization.
- **memory/**: Implements different types of memory, such as episodic, semantic, and procedural memory.
- **models/**: Contains model interfaces and implementations, such as ChatGPT interface.
- **tests/**: Placeholder for test cases.
- **workspace/**: Contains tools and work-related scripts.

## Detailed Descriptions

### agent/
- **__init__.py**: Initializes the agent module.
- **boostrap.py**: Bootstraps the agent.
- **idle_activities.py**: Manages idle activities for the agent.
- **main.py**: Main entry point for the agent.
- **message_handler.py**: Handles incoming messages.
- **task_manager.py**: Manages tasks for the agent.
- **utils.py**: Utility functions for the agent.

### agent_data/
- **agent_data.json**: Stores agent-related data.
- **episodic_memory/**: Stores episodic memory data.
- **semantic_memory/**: Stores semantic memory data.

### gpt/
- **chatgpt.py**: Implements ChatGPT functionalities.
- **llm_server.py**: Server for large language models.

### interfaces/
- **__init__.py**: Initializes the interfaces module.
- **http_server.py**: Implements an HTTP server.
- **user_interface.py**: Implements the user interface.

### llm/
- **extract_entity/**: Contains code for entity extraction.
- **generate_task_plan/**: Contains code for task planning.
- **reason/**: Contains code for reasoning.
- **summarize/**: Contains code for summarization.

### memory/
- **HuggingFaceEmbeddings/**: Implements HuggingFace embeddings.
- **Pooling.py**: Implements pooling for memory.
- **Transformer.py**: Implements transformer models for memory.
- **episodic_memory.py**: Implements episodic memory.
- **memory.py**: Core memory functionalities.
- **procedural_memory.py**: Implements procedural memory.
- **semantic_memory.py**: Implements semantic memory.

### models/
- **__init__.py**: Initializes the models module.
- **chatgpt_interface.py**: Implements ChatGPT interface.

### workspace/
- **toolbag/**: Contains toolbag scripts.
- **tools/**: Contains various tools for different tasks.
- **work/**: Placeholder for work-related scripts.

## How to Contribute

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

For more detailed information, refer to the `DETAILED_DOCUMENTATION.md` and `PROJECT_STRUCTURE.md` files.

## Bootstrap Agent

The `bootstrap.py` file in the `agent` directory is responsible for initializing and running the BootstrapAgent. The agent uses various types of memory (episodic, semantic, procedural) and tools to perform tasks and learn continuously. The main functionalities include:

- **Initialization**: Sets up the agent with default or provided configurations.
- **Continuous Learning Loop**: Keeps the agent running and learning from tasks and actions.
- **Task Management**: Generates, executes, and evaluates tasks.
- **Memory Management**: Stores and retrieves episodic, semantic, and procedural memories.
- **Tool Management**: Loads and memorizes tools for task execution.
- **Agent State Management**: Saves and loads the agent's state to and from disk.

