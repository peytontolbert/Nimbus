import os
import json
import logging
from typing import Dict


class toolmanagement:
    def __init__(self):
        logging.basicConfig(filename="toolmanagement.log", level=logging.INFO)
        self.tools_path = os.path.join(os.getcwd(), "workspace", "tools")
        self.tools = []
        self.load_tools()

    def load_tools(self, args=None):
        try:
            with open(os.path.join("workspace", "toolbag", "tools.json"), "r") as f:
                self.tools = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error: {e}")
            return f"Error: {e}"

    def create_tool(self, name, func, args, description, genre, function):
        if not all([name, func, args, description, genre]):
            return "All parameters must be provided."

        module_file = f"{genre}.py"
        module_path = os.path.join(self.tools_path, module_file)

        if os.path.exists(module_path):
            new_tool = {
                "name": name,
                "func": func,
                "args": args,
                "description": description,
                "class": genre,
                "user_permission_required": True,
            }
            self.tools.append(new_tool)
            self.save_tools()
        else:
            print(f"Warning: Tool module file {module_file} not found.")
            return "Tool Class does not exist. Try creating a new class first."

    def save_tools(self, args=None):
        try:
            with open(os.path.join("workspace", "toolbag", "tools.json"), "w") as f:
                json.dump(self.tools, f)
        except (FileNotFoundError, IOError) as e:
            logging.error(f"Error: {e}")
            return f"Error: {e}."
        # print("Error: File not found or unable to write file.")

    def list_by_class(self, class_name):
        if not class_name:
            print("Class name must be provided.")
            return "Class name must be provided."

        tools = [tool for tool in self.tools if tool["class"] == class_name]
        if not tools:
            print(f"No tools found for class '{class_name}'")
            return f"No tools found for class '{class_name}'"
        return tools

    def list_tool_classes(self, args=None):
        classes = [tool["class"] for tool in self.tools]
        classes = list(dict.fromkeys(classes))  # remove duplicates
        return classes

    def create_new_class(self, genre):
        string = str(genre)
        if not string or not string.isidentifier():
            error_message = "Invalid python class name."
            logging.error(error_message)
            return error_message

        file_path = os.path.join("workspace", "tools", f"{string}.py")
        try:
            with open(file_path, "w") as f:
                f.write(f"class {string}:\n")
                f.write(f"    def __init__(self):\n")
                f.write(f"        pass\n")
            return f"Created new class {string} in {file_path}"
        except (FileNotFoundError, IOError) as e:
            error_message = f"Unable to create class {string}."
            logging.error(error_message)
            return error_message


    def update_tool(self, name: str, new_description: str, new_func: str, new_args: Dict):
        """
        This tool allows you to update the details of an existing tool, such as its description, function, or arguments. It helps keep your tool definitions current and accurate.
        """
        tool = next((tool for tool in self.tools if tool["name"] == name), None)
        if tool:
            tool["description"] = new_description
            tool["func"] = new_func
            tool["args"] = new_args
            self.save_tools()
            return f"Tool '{name}' updated successfully."
        else:
            return f"Tool '{name}' not found."

    def delete_tool(self, name: str):
        """
        Use this tool to remove an existing tool from your collection. This is helpful for maintaining a clean and organized toolset by removing outdated or unnecessary tools.
        """
        tool = next((tool for tool in self.tools if tool["name"] == name), None)
        if tool:
            self.tools.remove(tool)
            self.save_tools()
            return f"Tool '{name}' deleted successfully."
        else:
            return f"Tool '{name}' not found."

    def clone_tool(self, original_name: str, new_name: str):
        """
        This tool allows you to create a copy of an existing tool with a new name. It is useful for creating similar tools with slight variations.
        """
        tool = next((tool for tool in self.tools if tool["name"] == original_name), None)
        if tool:
            new_tool = tool.copy()
            new_tool["name"] = new_name
            self.tools.append(new_tool)
            self.save_tools()
            return f"Tool '{original_name}' cloned successfully as '{new_name}'."
        else:
            return f"Tool '{original_name}' not found."

    def tool_usage_statistics(self):
        """
        Use this tool to view statistics on how often each tool is used. It helps identify the most and least used tools in your collection.
        """
        # Placeholder for tool usage statistics. This would typically require tracking usage data.
        # For simplicity, this function could return a mockup or random usage stats.
        usage_stats = {tool["name"]: 0 for tool in self.tools}  # Initialize all with zero usage
        # Logic to calculate actual usage would go here
        print("Tool Usage Statistics:")
        for tool_name, usage in usage_stats.items():
            print(f"Tool: {tool_name}, Usage: {usage} times")
        return usage_stats

    def export_tools(self, file_path: str):
        """
        This tool allows you to export your tools and their configurations to a file. It's useful for backing up your tools or sharing them with others.
        """
        try:
            with open(file_path, "w") as f:
                json.dump(self.tools, f, indent=4)
            return f"Tools exported successfully to {file_path}."
        except (FileNotFoundError, IOError) as e:
            logging.error(f"Error: {e}")
            return f"Error exporting tools: {e}."

    def import_tools(self, file_path: str):
        """
        Use this tool to import tools from a file into your current tool collection. This is helpful for restoring tools from a backup or integrating tools shared by others.
        """
        try:
            with open(file_path, "r") as f:
                imported_tools = json.load(f)
            self.tools.extend(imported_tools)
            self.save_tools()
            return f"Tools imported successfully from {file_path}."
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error: {e}")
            return f"Error importing tools: {e}."
