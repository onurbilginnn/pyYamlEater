from file_system.file_system import YamlFile

def main():
    file_contents = YamlFile('src/tests/test.yaml').read_file()
    for index, line in enumerate(file_contents):
        print(index,line[:-1])
if __name__ == "__main__":
    main()