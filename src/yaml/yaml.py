from yaml.constants import DEFAULT_INDENT_COUNT
from yaml.enums import YamlKeyCharacter, YamlRowType, YamlRowEndsWith

class YamlRow:
    def __init__(self, raw: str, sequence_number: int = 1):
       self.raw = raw
       self.sequence_number = sequence_number
       self.indent = self.find_indent()
       self.set_type(YamlRowType.KEY_VALUE)
       self.key_value = self.get_key_value()
       self.level = 0
       
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
        
    def get_key_value(self) -> tuple[str, str]:
        stripped_raw = self.raw.lstrip()
        if stripped_raw.startswith(YamlKeyCharacter.HYPHEN.value):
            if YamlKeyCharacter.COLON.value in stripped_raw:
                key, value = self.extract_key_value(stripped_raw)
                self.set_type(YamlRowType.ARRAY_ITEM_WITH_NESTED_KEYS) if value == "" or value == "" else self.set_type(YamlRowType.ARRAY_ITEM_WITH_VALUE)
                return key, value
            else:
                key, value = self.extract_key_value(stripped_raw)
                if value == YamlKeyCharacter.ONLY_COLON.value:
                    self.set_type(YamlRowType.ARRAY_ITEM_WITH_NESTED_KEYS)
                else:
                    self.set_type(YamlRowType.ARRAY_ITEM)
                return key, value
        else:
            if not YamlKeyCharacter.COLON.value in stripped_raw and not stripped_raw.endswith(YamlKeyCharacter.ONLY_COLON.value):
                raise ValueError(f"Error: Can not extract key in line {self.sequence_number}: {self.raw}")
        if stripped_raw.startswith(YamlKeyCharacter.SQUARE.value):
            self.set_type(YamlRowType.COMMENT)
            return stripped_raw, ""
        if YamlKeyCharacter.COLON.value in stripped_raw:
            key, value = self.extract_key_value(stripped_raw)
            if value == "" or value == YamlKeyCharacter.ONLY_COLON.value:
                self.set_type(YamlRowType.KEY_WITH_NESTED_KEYS)
            return key, value
        key, value = self.extract_key_value(stripped_raw)
        if value == YamlKeyCharacter.ONLY_COLON.value:
            self.set_type(YamlRowType.KEY_WITH_NESTED_KEYS)
        return key, value
    
    def __repr__(self):        
        return f"sequence number= {self.sequence_number}, raw= {self.raw}, indent= {self.indent}, key= {self.key_value[0]}, value= {self.key_value[1]}, type= {self.type}, level= {self.level}"
    
    def set_type(self, type: YamlRowType):
        self.type = type
    
    def extract_key_value(self, stripped_raw_text: str) -> tuple[str, str]:
        key_value = stripped_raw_text.split(YamlKeyCharacter.COLON.value, 1)
        key = key_value[0].strip()
        value = key_value[1].strip() if len(key_value) > 1 else ""
        if key.endswith(YamlRowEndsWith.COLON.value):
            key = key[:-1].strip()
            value = YamlKeyCharacter.ONLY_COLON.value
        return key, value
        

        
    
class Yaml:
    def __init__(self, raw_lines: list[str]):
        self.raw_lines = raw_lines
        self.yaml_rows = self.parse_yaml_rows()
    
    def parse_yaml_rows(self) -> list[YamlRow]:
        yaml_rows = []
        for index, line in enumerate(self.raw_lines):
            yaml_rows.append(YamlRow(line, index + 1))
        return yaml_rows
    
    # def validate_yaml(self) -> bool:
    #     array_indent = -1
    #     for index, current_row in enumerate(self.yaml_rows):
    #         current_key = current_row.key_value[0]
    #         if index == 0:
    #             continue
    #         previous_row = self.yaml_rows[index - 1]
    #         if current_row.indent > previous_row.indent and previous_row.key_value[1] != "" and array_indent == -1:
    #             raise ValueError(f"""Error: {previous_row.key_value[0]} 
    #                              can not have a value and nested keys at the same time in line 
    #                              {previous_row.sequence_number}""")
    #         if current_key.startswith(YamlKeyCharacter.HYPHEN.value + " "):
    #             if array_indent == -1 and current_row.indent < previous_row.indent:
    #                 raise ValueError(f"""Error: Array item can not be at lower level with its parent key in line 
    #                                  {current_row.sequence_number}""")
    #             if array_indent == -1:
    #                 array_indent = current_row.indent
    #             else:
    #                 if current_row.indent != array_indent:
    #                     raise ValueError(f"""Error: Array item must be at the same level in line 
    #                                      {current_row.sequence_number}""")
    #         else:
    #             if array_indent != -1 and current_row.indent <= array_indent:
    #                 array_indent = -1
    #     return True
        
    
    def __repr__(self):
        result = ""
        for yaml_row in self.yaml_rows:
            result += f"indent: {yaml_row.indent}, key: {yaml_row.key_value[0]}, value: {yaml_row.key_value[1] if yaml_row.key_value[1] != '' else 'EMPTY'}\n"
        return result
        
        
        
        