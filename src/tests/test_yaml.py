import unittest
from yaml.yaml import YamlRow

class TestTextNode(unittest.TestCase):
    def test_yaml_row_indent(self):
        test_yaml_row = YamlRow("find indent")
        self.assertEqual(test_yaml_row.find_indent(), 0)


if __name__ == "__main__":
    unittest.main()
