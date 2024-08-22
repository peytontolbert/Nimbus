from agent.message_handler import MessageHandler
from agent.task_manager import TaskManager
from memory.episodic_memory import EpisodicMemory
from memory.semantic_memory import SemanticMemory
from memory.procedural_memory import ProceduralMemory
from gpt.chatgpt import ChatGPT


def main():
    # Initialize components
    message_handler = MessageHandler()
    task_manager = TaskManager()
    episodic_memory = EpisodicMemory()
    semantic_memory = SemanticMemory()
    procedural_memory = ProceduralMemory()
    chatgpt_interface = ChatGPT()

    # Main loop
    while True:
        # Check for new messages
        message = message_handler.check_for_messages()
        if message:
            # Process message and manage tasks
            task_manager.handle_message(
                message,
                chatgpt_interface,
                episodic_memory,
                semantic_memory,
                procedural_memory,
            )

        # Perform idle activities if no tasks are pending
        if task_manager.is_idle():
            # Placeholder for idle activities
            pass


if __name__ == "__main__":
    main()
