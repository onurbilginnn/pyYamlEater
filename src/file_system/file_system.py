class FileSystem:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_file(self) -> str:
        with open(self.file_path, 'r') as file:
            return file.readlines()
    
    def write_file(self, content: str) -> None:
        with open(self.file_path, 'w') as file:
            file.write(content)
            
    def error_reading_file(self, error: str) -> None:
        raise ValueError(f"Error reading file: {error}")
            
class YamlFile(FileSystem):
    def __init__(self, file_path: str):
        if not file_path.endswith('.yaml') and not file_path.endswith('.yml'):
            self.error_reading_file("File must have a .yaml or .yml extension")
        super().__init__(file_path)
    