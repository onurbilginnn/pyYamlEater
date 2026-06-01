from yaml.yaml_row import YamlRow
from yaml.enums import YamlRowType, YamlKeyCharacter

class Yaml:
    def __init__(self, raw_lines: list[str]):
        if len(raw_lines) == 0:
            raise ValueError("YAML file cannot be empty.")
        self.raw_lines = raw_lines
        self.yaml_rows = self.parse_yaml_rows()
        self.root_indent = self.yaml_rows[0].indent
    
    def parse_yaml_rows(self) -> list[YamlRow]:
        yaml_rows = []
        index = 0
        line_number = 1
        while index < len(self.raw_lines):
            line = self.raw_lines[index]
            if line[:-1].strip() == "":
                index += 1
                line_number += 1
                continue
            yaml_row = YamlRow(line[:-1], line_number)
            if yaml_row.type == YamlRowType.KEY_VALUE_ON_NEXT_LINE:
                key, _ = yaml_row.key_value
                yaml_row.key_value = (key, "")
                j = index + 1
                while j < len(self.raw_lines):
                    next_line = self.raw_lines[j]
                    if next_line.strip() == "":
                        j += 1
                        continue
                    next_line_indent = YamlRow.find_indent(next_line)
                    if next_line_indent > yaml_row.indent:
                        k, v = yaml_row.key_value
                        v += next_line.strip() + "\n"
                        yaml_row.key_value = (k, v)
                        j += 1
                    else:
                        break
                k, v = yaml_row.key_value
                yaml_row.key_value = (k, v.rstrip("\n"))
                line_number += 1
                yaml_rows.append(yaml_row)
                index = j
                continue
            line_number += 1
            yaml_rows.append(yaml_row)
            index += 1
        return yaml_rows
    
    def validate_yaml(self):
        for index, current_row in enumerate(self.yaml_rows):
            next_row = self.yaml_rows[index + 1] if index < len(self.yaml_rows) - 1 else None
            if self.is_current_indent_lower_than_root(current_row):
                raise ValueError(f"Error: Can not add lower line indent than first line indent, key: {current_row.key_value[0]} at line: {current_row.line_number}")
            if self.does_key_value_item_have_child(current_row, next_row):
                raise ValueError(f"Error: Key value item can not have child item, key: {current_row.key_value[0]} at line: {current_row.line_number}")
            if self.does_child_has_lower_indent(current_row, next_row):
                raise ValueError(f"Error: Child item can not have lower indent than parent item, key: {current_row.key_value[0]} at line: {current_row.line_number}")
            if self.does_child_text_has_lower_indent(current_row, next_row):
                raise ValueError(f"Error: Child text item can not have lower indent than parent item, key: {current_row.key_value[0]} at line: {current_row.line_number}")

    def is_current_indent_lower_than_root(self, current_row: YamlRow) -> bool:
        return current_row.indent < self.root_indent
    
    def does_key_value_item_have_child(self, current_row: YamlRow, next_row: YamlRow) -> bool:
        return next_row and next_row.indent > current_row.indent and current_row.type == YamlRowType.KEY_VALUE
    
    def does_child_has_lower_indent(self, current_row: YamlRow, next_row: YamlRow) -> bool:
        return next_row and next_row.indent < current_row.indent and current_row.type == YamlRowType.KEY_WITH_NESTED_KEYS
    
    def does_child_text_has_lower_indent(self, current_row: YamlRow, next_row: YamlRow) -> bool:
        return next_row and next_row.indent < current_row.indent and current_row.key_value[1] == YamlKeyCharacter.VERTICALBAR.value
    
    def __repr__(self):
        result = ""
        for yaml_row in self.yaml_rows:
            result += f"{yaml_row}\n"
        return result
        
        