#converter.py
import json
import sys
import os

def parse_args():
    if len(sys.argv) != 3:
        print("Usage: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    input_ext = os.path.splitext(input_file)[1]
    output_ext = os.path.splitext(output_file)[1]

    if input_ext not in ['.xml', '.json', '.yml', '.yaml'] or output_ext not in ['.xml', '.json', '.yml', '.yaml']:
        print("Supported formats are: .xml, .json, .yml, .yaml")
        sys.exit(1)

    return input_file, output_file

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def write_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    input_file, output_file = parse_args()
    input_ext = os.path.splitext(input_file)[1]
    output_ext = os.path.splitext(output_file)[1]

    if input_ext == '.json':
        data = read_json(input_file)

    if output_ext == '.json':
        write_json(data, output_file)
