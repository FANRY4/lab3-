import os
import time

class File:
    def __init__(self, filename):
        self.filename = filename
        self.created_time = self.get_created_time()
        self.updated_time = self.created_time

    def get_created_time(self):
        return time.ctime(os.path.getctime(self.filename))

    def get_updated_time(self):
        return time.ctime(os.path.getmtime(self.filename))

    def update_snapshot(self):
        self.updated_time = self.get_updated_time()

    def get_info(self):
        raise NotImplementedError("Subclass must implement abstract method")

class TextFile(File):
    def __init__(self, filename):
        super().__init__(filename)
        self.line_count = self.word_count = self.character_count = 0

    def update_counts(self):
        with open(self.filename, 'r') as file:
            self.line_count = sum(1 for line in file)
            file.seek(0)
            self.word_count = sum(len(line.split()) for line in file)
            file.seek(0)
            self.character_count = sum(len(line) for line in file)

    def get_info(self):
        self.update_counts()
        return f"Text File: {self.filename}, Created: {self.created_time}, Updated: {self.updated_time}, Lines: {self.line_count}, Words: {self.word_count}, Characters: {self.character_count}"

class ImageFile(File):
    def __init__(self, filename):
        super().__init__(filename)
        self.width = self.height = 0

    def update_dimensions(self):
        if self.filename.lower().endswith(('png', 'jpg')):
            self.width = 1024
            self.height = 860

    def get_info(self):
        self.update_dimensions()
        return f"Image File: {self.filename}, Created: {self.created_time}, Updated: {self.updated_time}, Dimensions: {self.width}x{self.height}"

class FolderMonitor:
    def __init__(self):
        self.folder_path = None
        self.files = {}

    def add_file(self, filename):
        _, extension = os.path.splitext(filename)
        if extension.lower() in ('.txt',):
            self.files[filename] = TextFile(filename)
        elif extension.lower() in ('.png', '.jpg'):
            self.files[filename] = ImageFile(filename)

    def delete_file(self, filename):
        if filename in self.files:
            del self.files[filename]

    def commit(self):
        for file in self.files.values():
            file.update_snapshot()

    def info(self, filename):
        if filename == 'all':
            for file in self.files.values():
                print(file.get_info())
        elif filename in self.files:
            print(self.files[filename].get_info())
        else:
            print("File not found.")

    def status(self):
        for filename, file in self.files.items():
            if file.get_updated_time() != file.created_time:
                print(f"File '{filename}' has been changed since the last snapshot.")

def main():
    folder_monitor = FolderMonitor()

    # Get folder path from user
    folder_path = input("Enter the path to the folder you want to monitor: ")
    if not os.path.isdir(folder_path):
        print("Invalid folder path.")
        return

    folder_monitor.folder_path = folder_path

    for filename in os.listdir(folder_monitor.folder_path):
        if os.path.isfile(os.path.join(folder_monitor.folder_path, filename)):
            folder_monitor.add_file(filename)

    while True:
        action = input("Enter action (commit, info <filename>, status) or type 'exit' to terminate: ").split()
        if action[0] == 'commit':
            folder_monitor.commit()
        elif action[0] == 'info':
            if len(action) > 1:
                folder_monitor.info(action[1])
            else:
                folder_monitor.info('all')
        elif action[0] == 'status':
            folder_monitor.status()
        elif action[0] == 'exit':
            print("Exiting program...")
            break
        else:
            print("Invalid action.")

        time.sleep(5)

if __name__ == "__main__":
    main()
