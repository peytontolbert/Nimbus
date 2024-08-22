import os
import subprocess


class coding:
    def __init__(self):
        pass

    def create_py(self, name, code):
        print("Creating:", name)
        print(code)
        file_name = name
        file_contents = code

        try:
            # Generate a unique filename
            unique_filename = str(file_name) + ".py"

            # Get the current directory
            current_dir = os.getcwd()

            # Create the workspace folder path
            workspace_folder = os.path.join(current_dir, "workspace", "work")
            # Create the file path
            file_path = os.path.join(workspace_folder, unique_filename)

            # Write the contents to the file
            with open(file_path, "w") as file:
                file.write(file_contents)

            # Return the created file path
            return file_path

        except Exception as e:
            return str(e)

    def run_script(self, file_path):
        # Get the current directory
        current_dir = os.getcwd()

        # Create the workspace folder path
        workspace_folder = os.path.join(current_dir, "workspace")

        # Run the Python script using subprocess
        subprocess.run(["python", os.path.join(workspace_folder, file_path)])

    def edit_file(self, file_path, content):
        current_dir = os.getcwd()
        workspace_folder = os.path.join(current_dir, "workspace", "work")
        file = os.path.join(workspace_folder, file_path)
        with open(file, "w") as f:
            f.write(content)

    def read_file(self, file_path):
        current_dir = os.getcwd()
        workspace_folder = os.path.join(current_dir, "workspace", "work")
        file = os.path.join(workspace_folder, file_path)
        with open(file, "r") as f:
            return f.read()

    def view_workspace(self):
        current_dir = os.getcwd()
        workspace_folder = os.path.join(current_dir, "workspace", "work")
        files = os.listdir(workspace_folder)
        return files

    def view_files(self, path):
        current_dir = os.getcwd()
        workspace_folder = os.path.join(current_dir, "workspace", "work")
        files = os.listdir(os.path.join(workspace_folder, path))
        return files


    def run_py(self, name: str):
        """
        This tool allows you to execute a Python script that has been created, providing immediate feedback on its output or errors.
        """
        try:
            # Get the current directory
            current_dir = os.getcwd()
            workspace_folder = os.path.join(current_dir, "workspace", "work")
            file_path = os.path.join(workspace_folder, f"{name}.py")

            if os.path.exists(file_path):
                subprocess.run(["python", file_path])
                print(f"Executed script: {name}.py")
            else:
                print(f"The script {name}.py does not exist.")
        except Exception as e:
            print(f"An error occurred while executing {name}.py: {str(e)}")


    def debug_py(self, name: str):
        """
        Use this tool to debug a Python script, highlighting errors and suggesting possible fixes.
        """
        try:
            # Get the current directory
            current_dir = os.getcwd()
            workspace_folder = os.path.join(current_dir, "workspace", "work")
            file_path = os.path.join(workspace_folder, f"{name}.py")

            if os.path.exists(file_path):
                print(f"Debugging script: {name}.py")
                # For simplicity, we'll just use Pylint for static analysis
                result = subprocess.run(["pylint", file_path], capture_output=True, text=True)
                print(result.stdout)
            else:
                print(f"The script {name}.py does not exist.")
        except Exception as e:
            print(f"An error occurred while debugging {name}.py: {str(e)}")

    def list_py(self):
        """
        This tool lists all the Python scripts created within the current session or project, helping users keep track of their files.
        """
        try:
            current_dir = os.getcwd()
            workspace_folder = os.path.join(current_dir, "workspace", "work")
            files = [f for f in os.listdir(workspace_folder) if f.endswith('.py')]
            print("Python scripts in workspace:")
            for file in files:
                print(file)
            return files
        except Exception as e:
            print(f"An error occurred while listing Python scripts: {str(e)}")
            return []

    def delete_py(self, name: str):
        """
        This tool allows users to delete a specified Python script, helping manage and organize their workspace.
        """
        try:
            current_dir = os.getcwd()
            workspace_folder = os.path.join(current_dir, "workspace", "work")
            file_path = os.path.join(workspace_folder, f"{name}.py")

            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted script: {name}.py")
            else:
                print(f"The script {name}.py does not exist.")
        except Exception as e:
            print(f"An error occurred while deleting {name}.py: {str(e)}")

    def edit_py(self, name: str, new_code: str):
        """
        With this tool, you can modify an existing Python script by updating its code.
        """
        try:
            current_dir = os.getcwd()
            workspace_folder = os.path.join(current_dir, "workspace", "work")
            file_path = os.path.join(workspace_folder, f"{name}.py")

            if os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write(new_code)
                print(f"Edited script: {name}.py")
            else:
                print(f"The script {name}.py does not exist.")
        except Exception as e:
            print(f"An error occurred while editing {name}.py: {str(e)}")