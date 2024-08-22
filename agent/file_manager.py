import os
import json
import pickle

class FileManager:
    def __init__(self, dir: str = './agent_data'):
        self.dir = dir

    def _get_absolute_path(self, relative_path: str) -> str:
        return os.path.join(self.dir, relative_path)

    def _create_dir_if_not_exists(self, path: str) -> None:
        if not os.path.exists(path):
            os.makedirs(path)

    def _agent_data_exists(self) -> bool:
        return os.path.exists(os.path.join(self.dir, 'agent_data.json'))

    def save_data(self, filename: str, data: any) -> None:
        with open(self._get_absolute_path(filename), 'wb') as file:
            pickle.dump(data, file)

    def load_data(self, filename: str) -> any:
        with open(self._get_absolute_path(filename), 'rb') as file:
            return pickle.load(file)

    def save_json(self, filename: str, data: dict) -> None:
        with open(self._get_absolute_path(filename), 'w') as file:
            json.dump(data, file)

    def load_json(self, filename: str) -> dict:
        with open(self._get_absolute_path(filename), 'r') as file:
            return json.load(file)

