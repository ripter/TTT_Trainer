from glob import glob
from os import path, makedirs
import argparse
import json


def process_files(root_dir, file_pattern, out_file, preview=False):
    # Construct the file pattern
    file_glob = path.join(root_dir, file_pattern)
    file_names = glob(file_glob)

    # Preview functionality
    if preview:
        print(f'Preview Mode: Enabled')
        print(f'Glob pattern: {file_glob}')
        print(f'Files found: {file_names}')
        print(f'Total files to process: {len(file_names)}')

        # Check if it will append to an existing file or create a new one
        if path.exists(out_file):
            print(f'Output file "{out_file}" exists. Operation would append to this file.')
        else:
            print(f'Output file "{out_file}" does not exist. Operation would create this file.')
        return  # Exit the function to prevent actual processing

    # Ensure output directory exists
    out_dir = path.dirname(out_file)
    if not path.exists(out_dir):
        print(f"Creating output directory: {out_dir}")
        makedirs(out_dir)

    file_data = []

    # Turn each file into a JSON object
    for file_name in file_names:
        with open(file_name, "r") as file:
            file_contents = file.read()
            json_object = json.dumps({"text": file_contents})
            file_data.append(json_object)

    # Write all the data to a file
    with open(out_file, "a") as file:
        for item in file_data:
            file.write(item + '\n')

    print(f"{len(file_data)} JSON objects written to {out_file}")



if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Process text files by prefix and generate a .jsonl file. Ensure to wrap the glob pattern in quotes. For example, "*.txt" or "*.log".')
    parser.add_argument("pattern", type=str, help="Glob pattern to match files, enclosed in quotes. For example, \"*.txt\".")
    parser.add_argument("--data_dir", type=str, default="data/", help="Root folder to search for files using the pattern.")
    parser.add_argument("--out_file", type=str, default="all.jsonl", help="File to write the output to.")
    parser.add_argument("--preview", action="store_true", help="Preview the files to be processed and the operation summary without executing.")

    # Parse arguments
    args = parser.parse_args()

    # Call the function with command-line arguments
    process_files(args.data_dir, args.pattern, args.out_file, args.preview)
