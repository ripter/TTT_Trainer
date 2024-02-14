import json
import random
import argparse
import os

def split_jsonl(file_path, out_path, train_ratio=0.7, valid_ratio=0.15):
    """
    Splits a JSONL file into training, validation, and testing files.

    Parameters:
    - file_path: The path to the .jsonl file to split.
    - train_ratio: The fraction of the data to use for training.
    - valid_ratio: The fraction of the data to use for validation.
    """
    # Load the .jsonl file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Shuffle the lines to ensure random distribution
    random.shuffle(lines)

    # Calculate split indices
    total_lines = len(lines)
    train_end = int(total_lines * train_ratio)
    valid_end = train_end + int(total_lines * valid_ratio)

    # Split the data
    train_data = lines[:train_end]
    valid_data = lines[train_end:valid_end]
    test_data = lines[valid_end:]

    # Function to write splits to their respective files
    def write_split(filename, data):
        file_path = os.path.join(out_path, filename)
        with open(file_path, 'w') as file:
            for line in data:
                file.write(line)

    # Write the data to files
    os.path.join(out_path, 'train.jsonl')
    write_split('train.jsonl', train_data)
    write_split('valid.jsonl', valid_data)
    write_split('test.jsonl', test_data)

    print("Data split into train.jsonl, valid.jsonl, and test.jsonl successfully.")



if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Split a JSONL file into train, validation, and test sets.')
    parser.add_argument("file_path", type=str, help='Path to the .jsonl file to be split.')
    parser.add_argument("--data_dir", type=str, default="./", help='Path to the directory to save the split files.')
    parser.add_argument("--train_ratio", type=float, default=0.7, help='Fraction of data to use for training (default: 0.7).')
    parser.add_argument("--valid_ratio", type=float, default=0.15, help='Fraction of data to use for validation (default: 0.15).')

    # Parse arguments
    args = parser.parse_args()

    # Call the function with command-line arguments
    split_jsonl(
        args.file_path,
        out_path=args.data_dir,
        train_ratio=args.train_ratio, 
        valid_ratio=args.valid_ratio
        )

