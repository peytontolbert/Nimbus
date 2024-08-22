import os
import logging
import shutil

class filemanager:
    def __init__(self):
        try:
            self.files = self.view_workspace()
            print(self.files)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def view_file(self, file_path):
        current_dir = os.getcwd()
        workspace_folder = os.path.join(current_dir, "workspace", "work")
        file = os.path.join(workspace_folder, file_path)
        try:
            with open(file, "r") as f:
                return f.read()
        except FileNotFoundError:
            print(f"The file {file_path} does not exist.")
            return f"The file {file_path} does not exist."

    def view_workspace(self):
        current_dir = os.getcwd()
        workspace_folder = os.path.join(current_dir, "workspace", "work")
        try:
            files = os.listdir(workspace_folder)
            return files
        except FileNotFoundError:
            print(
                f"The workspace folder does not exist at location: {workspace_folder}"
            )
            return (
                f"The workspace folder does not exist at location: {workspace_folder}"
            )

    def view_files(self, path):
        current_dir = os.getcwd()
        workspace_folder = os.path.join(current_dir, "workspace", "work")
        full_path = os.path.join(workspace_folder, path)

        try:
            files = os.listdir(full_path)
            return files
        except FileNotFoundError as e:
            print(f"The specified path '{full_path}' does not exist.")
            return f"The specified path '{full_path}' does not exist."
            # raise Exception(f"The specified path '{full_path}' does not exist.")

    def edit_file(self, file_path, content):
        current_dir = os.getcwd()
        workspace_folder = os.path.join(current_dir, "workspace", "work")
        file = os.path.join(workspace_folder, file_path)
        try:
            with open(file, "w") as f:
                f.write(content)
        except FileNotFoundError as e:
            logging.error(f"Error: {e}")
            return f"Error: {e}."


    def search_files(self, keyword: str, path: str = None):
        """
        This tool allows you to search for files within your workspace or a specific directory based on a keyword or pattern. It helps in quickly locating files without manually browsing through folders.
        """
        current_dir = os.getcwd()
        workspace_folder = os.path.join(current_dir, "workspace", "work")
        search_path = os.path.join(workspace_folder, path) if path else workspace_folder

        try:
            matching_files = []
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if keyword in file:
                        matching_files.append(os.path.join(root, file))
            
            if matching_files:
                print(f"Files matching '{keyword}':")
                for file in matching_files:
                    print(file)
                return matching_files
            else:
                print(f"No files matching '{keyword}' were found.")
                return []

        except Exception as e:
            print(f"An error occurred while searching for files: {str(e)}")
            return []

    def upload_file(self, file_path: str):
        """
        This tool enables you to upload a file from your local system to your workspace. It is useful for adding new files to your project or workspace.
        """
        try:
            current_dir = os.getcwd()
            workspace_folder = os.path.join(current_dir, "workspace", "work")
            shutil.copy(file_path, workspace_folder)
            print(f"Uploaded {file_path} to workspace.")
        except Exception as e:
            print(f"An error occurred while uploading {file_path}: {str(e)}")

    def download_file(self, path: str):
        """
        This tool allows you to download a file from your workspace to your local system. It is useful for accessing files offline or sharing them outside the workspace.
        """
        try:
            current_dir = os.getcwd()
            workspace_folder = os.path.join(current_dir, "workspace", "work")
            file_path = os.path.join(workspace_folder, path)
            
            if os.path.exists(file_path):
                destination_path = os.path.join(current_dir, os.path.basename(path))
                shutil.copy(file_path, destination_path)
                print(f"Downloaded {path} to {destination_path}.")
            else:
                print(f"The file {path} does not exist in the workspace.")
        except Exception as e:
            print(f"An error occurred while downloading {path}: {str(e)}")

    def delete_file(self, path: str):
        """
        This tool enables you to delete a file from your workspace. It is helpful for removing unnecessary or outdated files to keep your workspace organized.
        """
        try:
            current_dir = os.getcwd()
            workspace_folder = os.path.join(current_dir, "workspace", "work")
            file_path = os.path.join(workspace_folder, path)

            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted {path} from workspace.")
            else:
                print(f"The file {path} does not exist.")
        except Exception as e:
            print(f"An error occurred while deleting {path}: {str(e)}")

    def rename_file(self, old_path: str, new_name: str):
        """
        This tool allows you to rename a file in your workspace. It is useful for updating file names to better reflect their content or purpose.
        """
        try:
            current_dir = os.getcwd()
            workspace_folder = os.path.join(current_dir, "workspace", "work")
            old_file_path = os.path.join(workspace_folder, old_path)
            new_file_path = os.path.join(workspace_folder, new_name)

            if os.path.exists(old_file_path):
                os.rename(old_file_path, new_file_path)
                print(f"Renamed {old_path} to {new_name}.")
            else:
                print(f"The file {old_path} does not exist.")
        except Exception as e:
            print(f"An error occurred while renaming {old_path} to {new_name}: {str(e)}")