import openai


class think:
    def __init__(self):
        pass

    def run(self, string):
        print("Thinking:")
        result = self.chat_with_gpt3(string)
        return result

    @staticmethod
    def chat_with_gpt3(prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {
                    "role": "system",
                    "content": "I am an artifical cognitive entity. I need to think about something. Only reply with a thought in first person.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.9,
        )
        return response["choices"][0]["message"]["content"]


    def run_idea_generation(self, topic: str, number_of_ideas: int) -> list:
        """
        This tool allows you to generate a list of creative ideas or solutions for a given topic or problem. It can help when you need multiple perspectives or approaches to a challenge.
        """
        prompt = f"Generate {number_of_ideas} creative ideas or solutions for the topic: {topic}."
        response = self.chat_with_gpt3(prompt)
        ideas = response.split("\n")
        return [idea.strip() for idea in ideas if idea.strip()]

    def run_text_analysis(self, text: str) -> str:
        """
        Use this tool to perform a detailed analysis of a given text or problem. It breaks down the content into key components and provides insights or summaries.
        """
        prompt = f"Perform a detailed analysis of the following text: {text}"
        response = self.chat_with_gpt3(prompt)
        return response

    def run_solution_evaluation(self, solution: str, criteria: list) -> str:
        """
        This tool evaluates the feasibility or effectiveness of a proposed solution or idea. It provides a score or feedback based on various criteria.
        """
        criteria_str = ", ".join(criteria)
        prompt = f"Evaluate the solution: {solution} based on the following criteria: {criteria_str}."
        response = self.chat_with_gpt3(prompt)
        return response

    def run_reflective_thinking(self, experience: str) -> str:
        """
        Use this tool to engage in reflective thinking about a past experience or decision. It helps in understanding lessons learned and future improvements.
        """
        prompt = f"Reflect on the following experience: {experience}. What lessons can be learned, and what improvements can be made in the future?"
        response = self.chat_with_gpt3(prompt)
        return response

    def run_prioritization(self, items: list, criteria: str) -> list:
        """
        This tool helps in prioritizing tasks, ideas, or solutions based on their importance or urgency. It provides a ranked list to focus on what matters most.
        """
        items_str = ", ".join(items)
        prompt = f"Prioritize the following items based on {criteria}: {items_str}."
        response = self.chat_with_gpt3(prompt)
        prioritized_list = response.split("\n")
        return [item.strip() for item in prioritized_list if item.strip()]

