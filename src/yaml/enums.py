from enum import Enum

class YamlKeyCharacter(Enum):
    ONLY_COLON = ":"
    COLON = ": "
    VERTICALBAR = "|"
    HYPHEN = "- "
    SQUARE = "# "


class YamlRowType(Enum):
    KEY_VALUE = 1
    KEY_VALUE_ON_NEXT_LINE = 2
    KEY_WITH_NESTED_KEYS = 3
    ARRAY_ITEM = 4
    ARRAY_ITEM_WITH_VALUE = 5
    ARRAY_ITEM_WITH_NESTED_KEYS = 6
    ONLY_VALUE = 7
    COMMENT = 8
    
class YamlRowEndsWith(Enum):
    COLON = ":"