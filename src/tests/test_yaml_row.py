import unittest

from yaml.enums import YamlRowType
from yaml.yaml_row import YamlRow

class TestTextNode(unittest.TestCase):
    def test_yaml_row_indent(self):
        test_yaml_row = YamlRow("find indent: ")
        self.assertEqual(test_yaml_row.indent, 0)
        test_yaml_row2 = YamlRow("  find indent: ")
        self.assertEqual(test_yaml_row2.indent, 2)
    
    def test_yaml_row_get_key_value_errors(self):
        with self.assertRaises(ValueError) as context:
            _ = YamlRow("find indent")
        self.assertIn(f"Error: Can not extract key in line", context.exception.args[0])
        with self.assertRaises(ValueError) as context:
            _ = YamlRow("test:abc")
        self.assertIn(f"Error: Can not extract key in line", context.exception.args[0])
        
    def test_yaml_row_get_key_value(self):
        test_yaml_row = YamlRow("find indent: ")
        self.assertEqual(test_yaml_row.key_value[0], "find indent")
        self.assertEqual(test_yaml_row.key_value[1], "")
        self.assertEqual(test_yaml_row.type, YamlRowType.KEY_WITH_NESTED_KEYS)
        test_yaml_row2 = YamlRow("find indent  : ")
        self.assertEqual(test_yaml_row2.key_value[0], "find indent")
        self.assertEqual(test_yaml_row2.key_value[1], "")
        self.assertEqual(test_yaml_row2.type, YamlRowType.KEY_WITH_NESTED_KEYS)
        test_yaml_row3 = YamlRow("find indent  : tester")
        self.assertEqual(test_yaml_row3.key_value[0], "find indent")
        self.assertEqual(test_yaml_row3.key_value[1], "tester")
        self.assertEqual(test_yaml_row3.type, YamlRowType.KEY_VALUE)
        test_yaml_row4 = YamlRow("test: tester")
        self.assertEqual(test_yaml_row4.key_value[0], "test")
        self.assertEqual(test_yaml_row4.key_value[1], "tester")
        self.assertEqual(test_yaml_row4.type, YamlRowType.KEY_VALUE)    
        test_yaml_row5 = YamlRow("test: |")
        self.assertEqual(test_yaml_row5.key_value[0], "test")
        self.assertEqual(test_yaml_row5.key_value[1], "|")
        self.assertEqual(test_yaml_row5.type, YamlRowType.KEY_VALUE_ON_NEXT_LINE)    
        test_yaml_row6 = YamlRow("- test")
        self.assertEqual(test_yaml_row6.key_value[0], "- test")
        self.assertEqual(test_yaml_row6.key_value[1], "")
        self.assertEqual(test_yaml_row6.type, YamlRowType.ARRAY_ITEM)    
        test_yaml_row7 = YamlRow("- test: value")
        self.assertEqual(test_yaml_row7.key_value[0], "- test")
        self.assertEqual(test_yaml_row7.key_value[1], "value")
        self.assertEqual(test_yaml_row7.type, YamlRowType.ARRAY_ITEM_WITH_VALUE)    
        test_yaml_row8 = YamlRow("# test: value")
        self.assertEqual(test_yaml_row8.key_value[0], "# test: value")
        self.assertEqual(test_yaml_row8.key_value[1], "")
        self.assertEqual(test_yaml_row8.type, YamlRowType.COMMENT)   
        test_yaml_row9 = YamlRow("- test:")
        self.assertEqual(test_yaml_row9.key_value[0], "- test")
        self.assertEqual(test_yaml_row9.key_value[1], ":")
        self.assertEqual(test_yaml_row9.type, YamlRowType.ARRAY_ITEM_WITH_NESTED_KEYS)   
        test_yaml_row10 = YamlRow("find indent:")
        self.assertEqual(test_yaml_row10.key_value[0], "find indent")
        self.assertEqual(test_yaml_row10.key_value[1], ":")
        self.assertEqual(test_yaml_row10.type, YamlRowType.KEY_WITH_NESTED_KEYS)
        test_yaml_row11 = YamlRow("- test: ")
        self.assertEqual(test_yaml_row11.key_value[0], "- test")
        self.assertEqual(test_yaml_row11.key_value[1], "")
        self.assertEqual(test_yaml_row11.type, YamlRowType.ARRAY_ITEM_WITH_NESTED_KEYS)       
        test_yaml_row12 = YamlRow("test: | ")
        self.assertEqual(test_yaml_row12.key_value[0], "test")
        self.assertEqual(test_yaml_row12.key_value[1], "|")
        self.assertEqual(test_yaml_row12.type, YamlRowType.KEY_VALUE_ON_NEXT_LINE)  
        test_yaml_row5 = YamlRow("- test: |")
        self.assertEqual(test_yaml_row5.key_value[0], "- test")
        self.assertEqual(test_yaml_row5.key_value[1], "|")
        self.assertEqual(test_yaml_row5.type, YamlRowType.ARRAY_ITEM_VALUE_ON_NEXT_LINE)      

if __name__ == "__main__":
    unittest.main()
