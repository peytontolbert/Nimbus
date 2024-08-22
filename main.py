import os
import threading
import importlib
from agent.bootstrap import BootstrapAgent
from dotenv import load_dotenv
from workspace.tools.base import AgentTool
from workspace.toolbag.toolbag import Toolbag

main_stop_event = threading.Event()  # Event object to stop the main script

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
AGENT_DIRECTORY = os.getenv("AGENT_DIRECTORY", "")
assert AGENT_DIRECTORY, "AGENT_DIRECTORY variable is missing from .env"

### 1.Create Agent ###
dir = AGENT_DIRECTORY

def main():
    try:
        print("agent starting up")
        finnagi = BootstrapAgent(
            dir=dir,
        )
        tools = []
        toolbag = Toolbag()
        print(toolbag)
        for tool in toolbag.toolbag:
            tools.append(tool)
        for tool in tools:
            module_name = tool['class']  # module name
            function_name = tool['func'].split('.')[-1]  # function name

            # load the module
            module = importlib.import_module(f"workspace.tools.{module_name}")

            # get the function
            classe = getattr(module, module_name)
            instance = classe()
            func = getattr(instance, function_name)

            #print(tool)
            tool_instance = AgentTool(
                name=tool['name'],
                func=func,
                args=tool['args'],
                description=tool['description'],
                user_permission_required=tool['user_permission_required']
            )
            print(tool_instance)
            finnagi.procedural_memory.memorize_tools([tool_instance])
        while not main_stop_event.is_set():
            try:
                finnagi.run()
            except KeyboardInterrupt:
                print("Exiting...")
            pass

            # Continue doing what the AGI was doing...
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
