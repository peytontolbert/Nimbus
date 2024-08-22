import openai
import os
from dotenv import load_dotenv
import time

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


class ChatGPT:
    def __init__(self):
        pass

    def process_thought(self, thought, message="", goal=""):
        system_prompt = """I am an artifical cognitive entity.
        I need to create thoughts to accomplish the task sent in a message.
        The processed thought will be the input to create a task list.\n"""
        prompt = """Thought: {thought}\n
        """
        if message:
            prompt += """Message: {message}\n\nProcessed thought:"""
        response = self.chat_with_gpt3(
            system_prompt, prompt.format(thought=thought, message=message)
        )
        print(response)
        return response

    @staticmethod
    def chat_with_gpt3(system_prompt, prompt, retries=5, delay=5):
        for i in range(retries):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.9,
                )
                return response["choices"][0]["message"]["content"]
            except openai.error.ServiceUnavailableError:
                if i < retries - 1:  # i is zero indexed
                    time.sleep(delay)  # wait before trying again
                else:
                    raise  # re-raise the last exception if all retries fail

    @staticmethod
    def chat_with_local_llm(system_prompt, prompt, retries=5, delay=5):
            import requests
            url = "http://localhost:5001/generate"
            payload = {"prompt": f"{system_prompt}\n{prompt}"}
            headers = {"Content-Type": "application/json"}
            for i in range(retries):
                try:
                    response = requests.post(url, json=payload, headers=headers)
                    response.raise_for_status()
                    return response.json()["response"]
                except requests.exceptions.RequestException as e:
                    if i < retries - 1:  # i is zero indexed
                        time.sleep(delay)  # wait before trying again
                    else:
                        raise e  # re-raise the last exception if all retries fail


    def chat_with_local_ollama(self, system_prompt, prompt, retries=5, delay=5):
        import requests
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.1",
            "prompt": f"{system_prompt}\n{prompt}",
            "format": "json",
            "stream": False
        }
        headers = {"Content-Type": "application/json"}
        for i in range(retries):
            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if i < retries - 1:  # i is zero indexed
                    time.sleep(delay)  # wait before trying again
                else:
                    raise e  # re-raise the last exception if all retries fail

