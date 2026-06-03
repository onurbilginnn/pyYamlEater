# pyYamlEater

A Python 3 YAML parser that reads `.yaml` files and converts them into Python dictionaries. Supports nested keys, arrays of scalar values, arrays of key-value objects, and multi-line (`|`) block values.

## Features

- Parses YAML files into Python `dict` structures
- Handles arbitrarily nested key/value pairs
- Supports hyphen-prefixed array items (`- value`, `- key: value`, `- key:` with nested children)
- Supports multi-line block values (`|`)
- Comments (`#`) are ignored
- Validates indentation consistency and structural correctness

## Supported YAML styles

```yaml
# Simple key-value
name: Alice

# Nested keys
address:
  city: LA
  country: USA

# Array of scalars
fruits:
  - apple
  - banana

# Array of objects
users:
  - name: Alice
    age: 30
  - name: Bob
    age: 25

# Multi-line block value
description: |
  This is a
  multi-line value
```

## Requirements

- Python 3.10+

## Run

```bash
./main.sh
```

This executes `python3 src/main.py`, which reads a YAML file and prints the parsed dictionary.

## Tests

```bash
./test.sh
```

This runs all unit tests via `unittest`:

```bash
python3 -m unittest discover -s src/tests -t src -v
```

## Project structure

```
src/
  main.py                  # Entry point
  yaml/
    yaml.py                # Core Yaml parser class
    yaml_row.py            # Parses individual YAML rows
    enums.py               # Row types and key character enums
    constants.py           # Default indent count
  file_system/
    file_system.py         # File reader (YamlFile)
  tests/
    test_yaml.py           # Test suite
    test_files/            # Sample valid and invalid YAML fixtures
```

