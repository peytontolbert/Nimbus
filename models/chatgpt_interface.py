import openai


class ChatGPTInterface:
    def __init__(self, api_key):
        openai.api_key = api_key

    def chat_with_llm(
        self, systemprompt: str, prompt: str, llm: str = "gpt-4o-2024-08-06"
    ):
        """
        Interacts with the LLM using the ChatCompletion API.

        :param systemprompt: The system message for the LLM
        :param prompt: The user prompt to send to the LLM
        :param llm: The model to use for completion
        :return: The generated response from the LLM
        """
        try:
            response = openai.ChatCompletion.create(
                model=llm,
                messages=[
                    {"role": "system", "content": systemprompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
            )
            return response["choices"][0]["message"]["content"]
        except openai.error.OpenAIError as e:
            print(f"Error generating response: {e}")
            return "Error generating response"
