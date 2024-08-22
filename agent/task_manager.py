class TaskManager:
    def __init__(self):
        self.tasks = []
        self.completed_tasks = []

    def handle_message(
        self,
        message,
        chatgpt_interface,
        episodic_memory,
        semantic_memory,
        procedural_memory,
    ):
        # Process the message to create a task
        task_description = self.process_message(message)
        if task_description:
            self.tasks.append(task_description)
            print(f"New task added: {task_description}")

            # Use ChatGPT to generate a response or action plan
            system_prompt = "You are a helpful assistant."
            response = chatgpt_interface.chat_with_llm(system_prompt, task_description)
            print(f"ChatGPT response: {response}")

            # Store the task and response in memory
            episodic_memory.store(task_description, response)

    def process_message(self, message):
        # Placeholder for message processing logic
        # Extract task description from the message
        return message.get("task_description", None)

    def is_idle(self):
        # Check if there are no pending tasks
        return len(self.tasks) == 0

    def add_task(self, task_description):
        self.tasks.append(task_description)
        print(f"Task added: {task_description}")

    def get_incomplete_tasks(self):
        return [task for task in self.tasks if task not in self.completed_tasks]

    def get_current_task_string(self):
        return self.tasks[0] if self.tasks else None

    def save_completed_tasks(self):
        self.completed_tasks.extend(self.tasks)
        self.tasks = []
        print("All tasks have been marked as completed.")

    def mark_task_complete(self, task_description):
        if task_description in self.tasks:
            self.tasks.remove(task_description)
            self.completed_tasks.append(task_description)
            print(f"Task marked as complete: {task_description}")

