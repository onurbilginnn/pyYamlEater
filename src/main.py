from pyYamlEater.src.file_system.file_system import YamlFile

def main():
    file_contents = YamlFile('test.yaml').read_file()
    print(file_contents)

if __name__ == "__main__":
    main()