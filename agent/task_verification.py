import openai
import json
from gpt.chatgpt import ChatGPT


class TaskVerifier:
    def __init__(self, api_key: str):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.gpt = ChatGPT()

    def verify_task_completion(self, action: str, action_result: str) -> bool:
        prompt = f"Action: {action}\nResult: {action_result}\nIs the task complete?"
        response = self.gpt.chat_with_local_ollama(system_prompt = "evaluate yes or no wether the task is complete", prompt = prompt)
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except Exception as e:
                print("Episodic memory data is corrupted.")
                raise e
        answer = response['response']
        return 'yes' in answer

