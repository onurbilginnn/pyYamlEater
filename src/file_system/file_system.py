from yaml.yaml import Yaml
from yaml.enums import YamlRowType, YamlKeyCharacter
from yaml.constants import DEFAULT_INDENT_COUNT


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
        
    def write_yaml_file(self, content: Yaml) -> None:
        text_content = ""
        formatted_content = content.format_yaml()
        for yaml_row in formatted_content:
            key, value = yaml_row.key_value
            if value == YamlKeyCharacter.ONLY_COLON.value:
                value = ""
            if yaml_row.type == YamlRowType.KEY_VALUE_ON_NEXT_LINE or yaml_row.type == YamlRowType.ARRAY_ITEM_VALUE_ON_NEXT_LINE:
                value = value.replace("\n", "\n" + " " * (yaml_row.indent + DEFAULT_INDENT_COUNT))
                text_content += " " * yaml_row.indent + key + ": |\n" + \
                " " * (yaml_row.indent + DEFAULT_INDENT_COUNT) + value + "\n"
            else:
                text_content += " " * yaml_row.indent + key + ": " + value + "\n"
        self.write_file(text_content)
    