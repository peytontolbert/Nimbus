import os
import json
import time
import traceback
from typing import Dict, Any, Optional, Union, List
from collections import deque
import openai
import pickle
import importlib
# Assuming you have these modules
import prompts.reason.prompt as ReasonPrompt
from prompts.reason.schema import JsonSchema as ReasonSchema
import prompts.summarize.prompt as SummarizePrompt
from prompts.json_output_parser import LLMJsonOutputParser
from memory.episodic_memory import EpisodicMemory, Episode
from workspace.tools.base import AgentTool
from memory.procedural_memory import ProceduralMemory
from memory.semantic_memory import SemanticMemory
from agent.task_manager import TaskManager
from gpt.chatgpt import ChatGPT
from agent.file_manager import FileManager

# Define the default values
DEFAULT_AGENT_NAME = "BootstrapAgent"
DEFAULT_AGENT_DIR = "./agent_data"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class BootstrapAgent:
    def __init__(self, dir: str = DEFAULT_AGENT_DIR, agent_name: str = DEFAULT_AGENT_NAME, gpt: Optional[ChatGPT] = None, procedural_memory: ProceduralMemory = ProceduralMemory(), episodic_memory: Optional[EpisodicMemory] = None, semantic_memory: Optional[SemanticMemory] = None, task_manager: Optional[TaskManager] = None, working_memory: Optional[deque] = deque(maxlen=12), thoughts: Optional[List[Any]] = [], messages: Optional[List[Any]] = [], last_task: Optional[str] = None) -> None:
        self.dir = dir
        self.agent_name = agent_name
        self.gpt = gpt if gpt is not None else ChatGPT()
        self.procedural_memory = procedural_memory
        self.episodic_memory = episodic_memory if episodic_memory is not None else EpisodicMemory()
        self.semantic_memory = semantic_memory if semantic_memory is not None else SemanticMemory()
        self.task_manager = task_manager if task_manager is not None else TaskManager()
        self.working_memory = working_memory
        self.thoughts = thoughts
        self.messages = messages
        self.last_task = last_task
        self.file_manager = FileManager()
        self.file_manager._get_absolute_path(DEFAULT_AGENT_DIR)
        self.file_manager._create_dir_if_not_exists(DEFAULT_AGENT_DIR)
        self.initialize_agent()

    def initialize_agent(self):
        if self.file_manager._agent_data_exists():
            self.load_agent()
        self.generate_initial_tasks()

    def run(self):
        """Main loop that keeps the agent running."""
        print(f"Running {self.agent_name}...")
        self.continuous_learning_loop()

    def load_and_memorize_tools(self):
        tools = self.load_tools_from_toolbag()
        for tool in tools:
            module_name = tool['class']
            function_name = tool['func'].split('.')[-1]
            module = importlib.import_module(f"workspace.tools.{module_name}")
            tool_class = getattr(module, module_name)
            instance = tool_class()
            func = getattr(instance, function_name)
            tool_instance = AgentTool(
                name=tool['name'],
                func=func,
                args=tool['args'],
                description=tool['description'],
                user_permission_required=tool['user_permission_required']
            )
            self.procedural_memory.memorize_tools([tool_instance])

    def generate_initial_tasks(self):
        initial_tasks = [
            "Explore file management tools",
            "Practice Coding",
            "Enhance memory management techniques",
            "Write Notes",
        ]
        for task in initial_tasks:
            self.task_manager.add_task(task)

    def continuous_learning_loop(self):
        while True:
            incomplete_tasks = self.task_manager.get_incomplete_tasks()
            while incomplete_tasks:
                current_task = self.task_manager.get_current_task_string()
                action, action_result = self.execute_action(current_task)
                self.working_memory.append(current_task)
                self.evaluate_and_learn(action, action_result)
                self.save_agent()  # Save agent's state after each step
                incomplete_tasks = self.task_manager.get_incomplete_tasks()
            self.task_manager.save_completed_tasks()
            self.generate_new_tasks()

    def execute_action(self, task_description: str) -> None:
        related_past_episodes = self.episodic_memory.remember_related_episodes(task_description, k=3)
        related_knowledge = self.semantic_memory.remember_related_knowledge(task_description, k=3) or "No related knowledge."
        tools = self.procedural_memory.remember_all_tools()
        tool_info = "\n".join([tool.get_tool_info() for tool in tools])
        memory = self.episodic_memory.remember_recent_episodes(2)
        # Prepare the input data for the prompt
        prompt_data = {
            "related_knowledge": related_knowledge,
            "related_past_episodes": related_past_episodes,
            "task": task_description,
            "tools": tool_info,
            "memory": memory
        }
        response = self.gpt.chat_with_local_ollama(
            system_prompt=ReasonPrompt.SCHEMA_TEMPLATE,
            prompt=ReasonPrompt.BASE_TEMPLATE.format(**prompt_data)
        )
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except json.JSONDecodeError as e:
                print(f"Failed to parse response as JSON: {e}")
                return
        action = response.get('action', {})
        action_result = self._act(action['tool'], action['args'])
        return action, action_result

    def evaluate_and_learn(self, action, action_result):
        try:
            prompt_data = {
                "action": action,
                "result": action_result
            }
            response = self.gpt.chat_with_local_ollama(
                system_prompt=SummarizePrompt.SCHEMA_TEMPLATE,
                prompt=SummarizePrompt.BASE_TEMPLATE.format(**prompt_data)
            )
            if isinstance(response, str):
                try:
                    response = json.loads(response)
                except json.JSONDecodeError as e:
                    print(f"Failed to parse act as JSON: {e}")
                    return
            self.process_evaluate_response(response, action, action_result)
        except Exception as e:
            print(f"Error in evaluation: {e}")
            return None

    def process_evaluate_response(self, response, action, action_result):
            print("Processing evaluation")
            evaluation_result = response['response']
            # If action is a string, parse it as JSON
            if isinstance(evaluation_result, str):
                try:
                    evaluation_result = json.loads(evaluation_result)
                except json.JSONDecodeError as e:
                    print(f"Failed to parse action as JSON: {e}")
                    return
            print(f"Evaluation Result: {evaluation_result}")
            # Store the evaluation result in memory
            self.store_memory(evaluation_result, action, action_result)


    def generate_new_tasks(self) -> None:
        """Generate new tasks based on the current state and memory."""
        new_task_prompt = "Generate new tasks based on the current state and memory."
        try:
            response = self.gpt.chat_with_local_ollama(
                system_prompt=ReasonPrompt.BASE_TEMPLATE,
                prompt=new_task_prompt
            )
            new_tasks = response['choices'][0]['message']['content'].split('\n')
            for task in new_tasks:
                self.task_manager.add_task(task)
            print(f"Generated New Tasks: {new_tasks}")
        except Exception as e:
            print(f"Error in generating new tasks: {e}")
            return None

    def store_memory(self, evaluation_result, action, result):
        if isinstance(action, str):
            try:
                action = json.loads(action)
            except json.JSONDecodeError as e:
                print(f"Failed to parse action as JSON: {e}")
                return
        thoughts = action.get('thoughts', '')
        summary = evaluation_result.get('summary', '')
        episode = Episode(thoughts, action, result, summary)
        self.episodic_memory.memorize_episode(episode)
        self.semantic_memory.extract_entity(evaluation_result)

    def save_agent(self):
        self.episodic_memory.save_local(DEFAULT_AGENT_DIR)
        self.semantic_memory.save_local(DEFAULT_AGENT_DIR)
        print("Agent saved successfully.")

    def save_agentold(self) -> None:
        episodic_memory_dir = f"{self.dir}/episodic_memory.pkl"
        semantic_memory_dir = f"{self.dir}/semantic_memory.pkl"
        filename = f"{self.dir}/agent_data.json"
        with open(episodic_memory_dir, 'wb') as episodic_file:
            pickle.dump(self.episodic_memory, episodic_file)
        with open(semantic_memory_dir, 'wb') as semantic_file:
            pickle.dump(self.semantic_memory, semantic_file)
        data = {"name": self.agent_name, "episodic_memory": episodic_memory_dir, "semantic_memory": semantic_memory_dir}
        with open(filename, "w") as f:
            json.dump(data, f)
        print("Agent saved successfully.")

    def load_agent(self) -> None:
        if not os.path.exists(os.path.join(self.dir, "agent_data.json")):
            print("Agent data does not exist.")
            return
        with open(os.path.join(self.dir, "agent_data.json")) as f:
            agent_data = json.load(f)
            self.agent_name = agent_data["name"]
            try:
                with open(agent_data["semantic_memory"], 'rb') as semantic_file:
                    self.semantic_memory = pickle.load(semantic_file)
            except Exception as e:
                print("Semantic memory data is corrupted.")
                raise e
            try:
                with open(agent_data["episodic_memory"], 'rb') as episodic_file:
                    self.episodic_memory = pickle.load(episodic_file)
            except Exception as e:
                print("Episodic memory data is corrupted.")
                raise e

    def _act(self, tool_name: str, args: Dict) -> str:
        # Get the tool to use from the procedural memory
        try:
            tool = self.procedural_memory.remember_tool_by_name(tool_name)
        except Exception as e:
            return "Invalid command: " + str(e)
        try:
            result = tool.run(**args)
            print(f"action result: {result}")
            self.working_memory.append(result)
            return result
        except Exception as e:
            return "Could not run tool: " + str(e)

