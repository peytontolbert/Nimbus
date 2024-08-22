import time
import json


class notes:
    def __init__(self):
        pass

    def write(self, string, file_path="notebook.json"):
        print("Writing notes:")
        entry = {"entry": string}
        self.write_to_notebook(entry, file_path)
        return entry

    def write_to_notebook(self, entry, file_path="notebook.json"):
        entries = self.read_all(file_path)
        entries.append(entry)
        with open(file_path, "w") as f:
            json.dump(entries, f)

    def read(self, index, file_path="notebook.json"):
        print(f"Reading note at index {index}:")
        entries = self.read_all(file_path)
        try:
            return entries[index]
        except IndexError:
            print(f"No note at index {index}")
            return None

    def read_all(self, file_path="notebook.json"):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def search(self, query: str, file_path="notebook.json"):
        """
        This tool allows you to search for specific keywords or phrases within your notes. It's useful for quickly finding information without manually scanning through all entries.
        """
        entries = self.read_all(file_path)
        matching_entries = [
            entry for entry in entries if query.lower() in entry["entry"].lower()
        ]
        if matching_entries:
            print(f"Found {len(matching_entries)} entries matching '{query}':")
            for entry in matching_entries:
                print(entry)
        else:
            print(f"No entries found matching '{query}'.")
        return matching_entries

    def delete(self, index: int, file_path="notebook.json"):
        """
        Use this tool to delete a specific note. It's helpful for managing your notes and removing outdated or irrelevant information.
        """
        entries = self.read_all(file_path)
        try:
            removed_entry = entries.pop(index)
            with open(file_path, "w") as f:
                json.dump(entries, f, indent=4)
            print(f"Deleted note at index {index}: {removed_entry}")
            return removed_entry
        except IndexError:
            print(f"No note at index {index} to delete.")
            return None

    def edit(self, index: int, new_content: str, file_path="notebook.json"):
        """
        This tool enables you to edit an existing note. It's perfect for updating information or correcting mistakes in your notes.
        """
        entries = self.read_all(file_path)
        try:
            entries[index]["entry"] = new_content
            entries[index]["edited_timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            with open(file_path, "w") as f:
                json.dump(entries, f, indent=4)
            print(f"Edited note at index {index}: {entries[index]}")
            return entries[index]
        except IndexError:
            print(f"No note at index {index} to edit.")
            return None

    def list(self, file_path="notebook.json"):
        """
        This tool provides a list of all your notes, displaying their titles or a brief snippet. It's useful for getting an overview of your notes and selecting which one to read or edit.
        """
        entries = self.read_all(file_path)
        print("Listing all notes:")
        for i, entry in enumerate(entries):
            snippet = entry["entry"][:30] + "..." if len(entry["entry"]) > 30 else entry["entry"]
            print(f"{i}: {snippet} (Created: {entry['timestamp']})")
        return entries

    def tag(self, index: int, tags: list, file_path="notebook.json"):
        """
        With this tool, you can add tags to your notes for better organization and easy retrieval based on categories or topics.
        """
        entries = self.read_all(file_path)
        try:
            if "tags" not in entries[index]:
                entries[index]["tags"] = []
            entries[index]["tags"].extend(tags)
            with open(file_path, "w") as f:
                json.dump(entries, f, indent=4)
            print(f"Added tags to note at index {index}: {tags}")
            return entries[index]
        except IndexError:
            print(f"No note at index {index} to tag.")
            return None