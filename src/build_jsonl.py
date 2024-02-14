import json
import argparse
from glob import glob
from os import path
from src.consts import DIR_OUTPUT

def process_files(file_prefix):
    # Construct the file pattern
    file_glob = path.join(DIR_OUTPUT, f'{file_prefix}*.txt')
    file_names = glob(file_glob)
    file_data = []

    # Turn each file into a JSON object
    for file_name in file_names:
        with open(file_name, "r") as file:
            file_contents = file.read()
            json_object = json.dumps({"text": file_contents})
            file_data.append(json_object)

    # Write all the data to a file
    data_file_path = path.join(DIR_OUTPUT, f'all_{file_prefix}.jsonl')
    with open(data_file_path, "a") as file:
        for item in file_data:
            file.write(item + '\n')

    print(f"Data written to {data_file_path}")


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Process text files by prefix and generate a .jsonl file.')
    parser.add_argument('file_prefix', type=str, help='Prefix of the files to process.')

    # Parse arguments
    args = parser.parse_args()

    # Call the function with command-line arguments
    process_files(args.file_prefix)
