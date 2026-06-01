from yaml.constants import DEFAULT_INDENT_COUNT
from yaml.enums import YamlKeyCharacter, YamlRowType, YamlRowEndsWith

class YamlRow:
    def __init__(self, raw: str, line_number: int = 1):
       self.raw = raw
       self.line_number = line_number
       self.indent = self.find_indent(raw)
       self.set_type(YamlRowType.KEY_VALUE)
       self.key_value = self.get_key_value()
       self.level = 0
    
    @staticmethod
    def find_indent(text: str) -> int:
        count = 0
        for char in text:
            if char == ' ':
                count += 1
            else:
                break
        if count % DEFAULT_INDENT_COUNT != 0:
            count += 1
        return count
        
    def get_key_value(self) -> tuple[str, str]:
        stripped_raw = self.raw.lstrip()
        if self.is_array_related_row(stripped_raw):
            if YamlKeyCharacter.COLON.value in stripped_raw:
                key, value = self.extract_key_value(stripped_raw)
                self.set_type(YamlRowType.ARRAY_ITEM_WITH_NESTED_KEYS) if value == "" else self.set_type(YamlRowType.ARRAY_ITEM_WITH_VALUE)
                return key, value
            else:
                key, value = self.extract_key_value(stripped_raw)
                if value == YamlKeyCharacter.ONLY_COLON.value:
                    self.set_type(YamlRowType.ARRAY_ITEM_WITH_NESTED_KEYS)
                else:
                    self.set_type(YamlRowType.ARRAY_ITEM)
                return key, value
        else:
            if self.should_raise_error(stripped_raw):
                raise ValueError(f"Error: Can not extract key in line {self.line_number}: {self.raw}")
        if stripped_raw.startswith(YamlKeyCharacter.SQUARE.value):
            self.set_type(YamlRowType.COMMENT)
            return stripped_raw, ""
        if YamlKeyCharacter.COLON.value in stripped_raw:
            key, value = self.extract_key_value(stripped_raw)
            if value == "":
                self.set_type(YamlRowType.KEY_WITH_NESTED_KEYS)
            if value == YamlKeyCharacter.VERTICALBAR.value:
                self.set_type(YamlRowType.KEY_VALUE_ON_NEXT_LINE)
            return key, value
        key, value = self.extract_key_value(stripped_raw)
        if value == YamlKeyCharacter.ONLY_COLON.value:
            self.set_type(YamlRowType.KEY_WITH_NESTED_KEYS)
        return key, value
    
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
    
    def is_array_related_row(self, stripped_raw: str) -> bool:
        return stripped_raw.startswith(YamlKeyCharacter.HYPHEN.value)
    
    def should_raise_error(self, stripped_raw: str) -> bool:
        return not YamlKeyCharacter.COLON.value in stripped_raw and not stripped_raw.endswith(YamlKeyCharacter.ONLY_COLON.value)

    def __repr__(self):        
        return f"line number= {self.line_number}, indent= {self.indent}, key= {self.key_value[0]}, value= {self.key_value[1]}, type= {self.type}, level= {self.level}"
            
        