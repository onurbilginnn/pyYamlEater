from file_system.file_system import FileSystem

def main():
    file_contents = FileSystem('README.md').read_file()
    print(file_contents)

if __name__ == "__main__":
    main()