from pyYamlEater.src.yaml.constants import DEFAULT_INDENT_COUNT

class YamlRow:
    def __init__(self, raw: str, key: str, value: str | int = None):
       self.raw = raw
       self.indent_count = self.find_indent()
       
    def find_indent(self) -> int:
        count = 0
        for char in self.raw:
            if char == ' ':
                count += 1
            else:
                break
        if count % DEFAULT_INDENT_COUNT != 0:
            count += 1
        return count
        

class Yaml:
    def __init__(self, rows: list[YamlRow]):
        self.rows = rows