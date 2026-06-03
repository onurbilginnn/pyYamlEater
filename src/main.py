from file_system.file_system import YamlFile
from yaml.yaml import Yaml

def main():
    yaml_file_path = "src/tests/test_files/valid_file7.yaml"
    yaml_contents = YamlFile(yaml_file_path).read_file()
    yaml = Yaml(yaml_contents)
    yaml_dict = yaml.convert_yaml_to_dict()
    print(yaml_dict)
    
if __name__ == "__main__":
    main()