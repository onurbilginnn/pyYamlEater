import unittest

from file_system.file_system import YamlFile
from yaml.enums import YamlRowType
from yaml.yaml import Yaml

class TestTextNode(unittest.TestCase):
    def test_yaml_parser_errors(self):
        invalid_yaml_contents = YamlFile('src/tests/test_files/invalid_file4.yaml').read_file()
        with self.assertRaises(ValueError) as context:
          Yaml(invalid_yaml_contents)
        self.assertIn("Error: Can not extract key in line", context.exception.args[0])
        
    def test_yaml_parser(self):
        valid_yaml_contents = YamlFile('src/tests/test_files/valid_file.yaml').read_file()
        yaml = Yaml(valid_yaml_contents)
        self.assertEqual(yaml.yaml_rows[0].type, YamlRowType.KEY_WITH_NESTED_KEYS)
        self.assertEqual(yaml.yaml_rows[0].key_value[0], "all")
        self.assertEqual(yaml.yaml_rows[17].key_value[0], "network1")
        self.assertEqual(yaml.yaml_rows[0].type, YamlRowType.KEY_WITH_NESTED_KEYS)
        self.assertEqual(yaml.yaml_rows[0].type, YamlRowType.KEY_WITH_NESTED_KEYS)
        print(yaml)
        valid_yaml_contents2 = YamlFile('src/tests/test_files/valid_file3.yaml').read_file()
        yaml2 = Yaml(valid_yaml_contents2)
        self.assertEqual(yaml2.yaml_rows[20].type, YamlRowType.ARRAY_ITEM_WITH_NESTED_KEYS)
        self.assertEqual(yaml2.yaml_rows[20].key_value[0], "- ip2")
        self.assertEqual(yaml2.yaml_rows[22].key_value[0], "network2")
        self.assertEqual(yaml2.yaml_rows[22].type, YamlRowType.KEY_WITH_NESTED_KEYS)
        valid_yaml_contents4 = YamlFile('src/tests/test_files/valid_file4.yaml').read_file()
        yaml4 = Yaml(valid_yaml_contents4)
        self.assertEqual(yaml4.yaml_rows[14].type, YamlRowType.KEY_VALUE_ON_NEXT_LINE)
        self.assertEqual(yaml4.yaml_rows[14].key_value[1], "tester:\nand_tested:\n- list item 1\n- list item 2")
        valid_yaml_contents5 = YamlFile('src/tests/test_files/valid_file6.yaml').read_file()
        yaml5 = Yaml(valid_yaml_contents5)
        self.assertEqual(yaml5.yaml_rows[17].type, YamlRowType.ARRAY_ITEM)
        self.assertEqual(yaml5.yaml_rows[15].type, YamlRowType.KEY_WITH_NESTED_KEYS)
        valid_yaml_contents6 = YamlFile('src/tests/test_files/valid_file7.yaml').read_file()
        yaml6 = Yaml(valid_yaml_contents6)
        self.assertEqual(yaml6.yaml_rows[16].type, YamlRowType.ARRAY_ITEM_VALUE_ON_NEXT_LINE)
        self.assertEqual(yaml6.yaml_rows[16].key_value[1], "where is my ip\nis it fine")
    
        
    def test_yaml_parser_array(self):
        valid_yaml_contents = YamlFile('src/tests/test_files/valid_file_array.yaml').read_file()
        yaml = Yaml(valid_yaml_contents)
        
    def test_validate_yaml_array_errors(self):
        invalid_yaml_contents = YamlFile('src/tests/test_files/invalid_file_array.yaml').read_file()
        yaml = Yaml(invalid_yaml_contents)
        with self.assertRaises(ValueError) as context:
            yaml.validate_yaml()
        self.assertIn("Error: List items can not have lower indent than parent list key, key:", context.exception.args[0])

    def test_validate_yaml_errors(self):
        invalid_yaml_contents = YamlFile('src/tests/test_files/invalid_file.yaml').read_file()
        yaml = Yaml(invalid_yaml_contents)
        with self.assertRaises(ValueError) as context:
            yaml.validate_yaml()
        self.assertIn("Error: Can not add lower line indent than first line indent", context.exception.args[0])
        invalid_yaml_contents2 = YamlFile('src/tests/test_files/invalid_file2.yaml').read_file()
        yaml2 = Yaml(invalid_yaml_contents2)
        with self.assertRaises(ValueError) as context:
            yaml2.validate_yaml()
        self.assertIn("Error: Key value item can not have child item", context.exception.args[0])
        invalid_yaml_contents3 = YamlFile('src/tests/test_files/invalid_file3.yaml').read_file()
        yaml3 = Yaml(invalid_yaml_contents3)
        with self.assertRaises(ValueError) as context:
            yaml3.validate_yaml()
        self.assertIn("Error: Child item can not have lower indent than parent item", context.exception.args[0])
       


if __name__ == "__main__":
    unittest.main()
