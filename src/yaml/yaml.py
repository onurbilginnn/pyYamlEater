from yaml.yaml_row import YamlRow
from yaml.enums import YamlRowType, YamlKeyCharacter
from yaml.constants import DEFAULT_INDENT_COUNT

class Yaml:
    def __init__(self, raw_lines: list[str]):
        if len(raw_lines) == 0:
            raise ValueError("YAML file cannot be empty.")
        self.raw_lines = raw_lines
        self.yaml_rows = self.parse_yaml_rows()
        self.root_indent = self.yaml_rows[0].indent
        self.validate_yaml()
        self.find_row_levels()


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
            updated_line = line[:-1] if index < len(self.raw_lines) - 1 else line
            yaml_row = YamlRow(updated_line, line_number)
            if yaml_row.type == YamlRowType.COMMENT:
                index += 1
                continue
            if yaml_row.type == YamlRowType.KEY_VALUE_ON_NEXT_LINE or \
               yaml_row.type == YamlRowType.ARRAY_ITEM_VALUE_ON_NEXT_LINE:
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
        yaml_list_start_indent = -1
        for index, current_row in enumerate(self.yaml_rows):
            next_row = self.yaml_rows[index + 1] if index < len(self.yaml_rows) - 1 else None
            if self.is_array_item(current_row):
                # Entering to list
                if yaml_list_start_indent == -1:
                    yaml_list_start_indent = current_row.indent
                elif current_row.indent != yaml_list_start_indent:
                    raise ValueError(f"Error: List items can not have lower indent than parent list key, key: {current_row.key_value[0]} at line: {current_row.line_number}")
            else:
                # Exit from list
                if yaml_list_start_indent != -1 and current_row.indent < yaml_list_start_indent:
                    yaml_list_start_indent = -1
            if self.is_current_indent_lower_than_root(current_row):
                raise ValueError(f"Error: Can not add lower line indent than first line indent, key: {current_row.key_value[0]} at line: {current_row.line_number}")
            if self.does_key_value_item_have_child(current_row, next_row):
                raise ValueError(f"Error: Key value item can not have child item, key: {current_row.key_value[0]} at line: {current_row.line_number}")
            if self.does_child_has_lower_indent(current_row, next_row):
                raise ValueError(f"Error: Child item can not have lower indent than parent item, key: {current_row.key_value[0]} at line: {current_row.line_number}")
            if self.does_child_text_has_lower_indent(current_row, next_row):
                raise ValueError(f"Error: Child text item can not have lower indent than parent item, key: {current_row.key_value[0]} at line: {current_row.line_number}")

    def find_row_levels(self):
        for index, current_row in enumerate(self.yaml_rows):
            previous_row = self.yaml_rows[index - 1] if index > 0 else None
            if current_row.indent == self.root_indent:
                current_row.level = 1
            elif previous_row and current_row.indent > previous_row.indent:
                current_row.level = previous_row.level + 1
            elif previous_row and current_row.indent == previous_row.indent:
                current_row.level = previous_row.level
            elif previous_row and current_row.indent < previous_row.indent:
                for pre_row in self.yaml_rows[:index -1]:
                    if pre_row.indent == current_row.indent:
                        current_row.level = pre_row.level
                        break
  
    def format_yaml(self) -> list[YamlRow]:
        formatted_yaml_rows: list[YamlRow] = []
        for index, current_row in enumerate(self.yaml_rows):
            previous_row = self.yaml_rows[index - 1] if index > 0 else None
            if index == 0:
                current_row.indent = 0
            elif previous_row and current_row.level > previous_row.level:
                current_row.indent = previous_row.indent + DEFAULT_INDENT_COUNT
            elif previous_row and current_row.level == previous_row.level:
                current_row.indent = previous_row.indent
            elif previous_row and current_row.level < previous_row.level:
                level_diff = previous_row.level - current_row.level
                current_row.indent = previous_row.indent - (DEFAULT_INDENT_COUNT * level_diff)
            formatted_yaml_rows.append(current_row)
        return formatted_yaml_rows
    
    
    def convert_yaml_to_dict(self) -> dict[str, str | dict]:
        yaml_dict: dict[str, str | dict] = {}
        formatted_yaml = self.format_yaml()
        level_map: dict[int, dict] = {0: yaml_dict}
        list_start_level = -1
        current_list = None

        for index, current_row in enumerate(formatted_yaml):
            lvl = current_row.level
            key = current_row.key_value[0]
            raw_val = current_row.key_value[1]
            val = None if raw_val == "" or raw_val == YamlKeyCharacter.ONLY_COLON.value else raw_val
            next_row = formatted_yaml[index + 1] if index < len(formatted_yaml) - 1 else None
            list_start_level = self.find_list_start_level(list_start_level, current_row, next_row)
            is_row_list_item = current_row.key_value[0].startswith(YamlKeyCharacter.HYPHEN.value)
            parent = level_map.get(lvl - 1, yaml_dict)
            if list_start_level == -1:
                self.add_key_value_to_dict(level_map, lvl, parent, key, val)
            elif list_start_level > -1 and current_row.level == list_start_level:
                parent[key] = []
                current_list = parent[key]
            elif list_start_level > -1 and is_row_list_item and current_list is not None:
                actual_key = key.removeprefix(YamlKeyCharacter.HYPHEN.value)
                if current_row.type == YamlRowType.ARRAY_ITEM:
                    current_list.append(actual_key)
                elif current_row.type == YamlRowType.ARRAY_ITEM_WITH_VALUE:
                    item = {actual_key: val}
                    current_list.append(item)
                    level_map[lvl] = item
                elif current_row.type == YamlRowType.ARRAY_ITEM_WITH_NESTED_KEYS:
                    item = {actual_key: {}}
                    current_list.append(item)
                    level_map[lvl] = item[actual_key]
                elif current_row.type == YamlRowType.ARRAY_ITEM_VALUE_ON_NEXT_LINE:
                    item = {actual_key: val}
                    current_list.append(item)
                    level_map[lvl] = item
            elif list_start_level > -1 and not is_row_list_item:
                self.add_key_value_to_dict(level_map, lvl, parent, key, val)

        return yaml_dict
    
    @staticmethod
    def add_key_value_to_dict(level_map: dict[int, dict], lvl: int, parent: dict[str, str | dict], key: str, value: str | dict) -> None:
            if value is None:
                if key not in parent:
                    parent[key] = {}
                level_map[lvl] = parent[key]
            else:
                parent[key] = value
    
    @staticmethod
    def find_list_start_level(list_start_level: int,current_row: YamlRow, next_row: YamlRow) -> int:
        if next_row and \
            next_row.key_value[0].startswith(YamlKeyCharacter.HYPHEN.value) and \
                list_start_level == -1 and not \
                    current_row.key_value[0].startswith(YamlKeyCharacter.HYPHEN.value):
            list_start_level = current_row.level
        elif list_start_level != -1 and \
            current_row.level <= list_start_level and not\
                current_row.key_value[0].startswith(YamlKeyCharacter.HYPHEN.value):
            list_start_level = -1
        return list_start_level
            
    def add_dict_value(self, yaml_dict: dict[str, str | dict], key: str, value: str | dict) -> None:
        yaml_dict[key] = value
            
    
    def is_current_indent_lower_than_root(self, current_row: YamlRow) -> bool:
        return current_row.indent < self.root_indent
    
    def does_key_value_item_have_child(self, current_row: YamlRow, next_row: YamlRow) -> bool:
        return next_row and next_row.indent > current_row.indent and current_row.type == YamlRowType.KEY_VALUE
    
    def does_child_has_lower_indent(self, current_row: YamlRow, next_row: YamlRow) -> bool:
        return next_row and next_row.indent < current_row.indent and current_row.type == YamlRowType.KEY_WITH_NESTED_KEYS
    
    def does_child_text_has_lower_indent(self, current_row: YamlRow, next_row: YamlRow) -> bool:
        return next_row and next_row.indent < current_row.indent and current_row.key_value[1] == YamlKeyCharacter.VERTICALBAR.value
    
    def is_array_item(self, current_row: YamlRow) -> bool:
        return current_row.type == YamlRowType.ARRAY_ITEM or \
                current_row.type == YamlRowType.ARRAY_ITEM_WITH_VALUE or \
                current_row.type == YamlRowType.ARRAY_ITEM_WITH_NESTED_KEYS or \
                current_row.type == YamlRowType.ARRAY_ITEM_VALUE_ON_NEXT_LINE

    
    def __repr__(self):
        result = ""
        for yaml_row in self.yaml_rows:
            result += f"{yaml_row}\n"
        return result
        
        