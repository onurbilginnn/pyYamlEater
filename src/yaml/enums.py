from enum import Enum

class YamlKeyCharacter(Enum):
    ONLY_COLON = ":"
    COLON = ": "
    VERTICALBAR = "|"
    HYPHEN = "- "
    SQUARE = "# "
    ONLY_SQUARE = "#"


class YamlRowType(Enum):
    KEY_VALUE = 1
    KEY_VALUE_ON_NEXT_LINE = 2
    KEY_WITH_NESTED_KEYS = 3
    ARRAY_ITEM = 4
    ARRAY_ITEM_WITH_VALUE = 5
    ARRAY_ITEM_WITH_NESTED_KEYS = 6
    ARRAY_ITEM_VALUE_ON_NEXT_LINE = 7
    ONLY_VALUE = 8
    COMMENT = 9
    
class YamlRowEndsWith(Enum):
    COLON = ":"