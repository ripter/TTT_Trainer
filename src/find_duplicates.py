import argparse
import hashlib
from glob import glob
from os import path

def hash_file_contents(file_path):
    """Generate a hash for the contents of a file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as file:
        content = file.read()
        hasher.update(content)
    return hasher.hexdigest()

def find_duplicates(folder, file_prefix):
    """Find and report files with identical contents."""
    file_glob = path.join(folder, f'{file_prefix}*.txt')
    file_names = glob(file_glob)
    content_hash_map = {}

    # Hash the contents of each file and store them in a map
    for file_name in file_names:
        file_hash = hash_file_contents(file_name)
        if file_hash in content_hash_map:
            content_hash_map[file_hash].append(file_name)
        else:
            content_hash_map[file_hash] = [file_name]

    # Report duplicates
    for files in content_hash_map.values():
        if len(files) > 1:
            print(f"Duplicate files found: {', '.join(files)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Find text files with identical contents based on a filename prefix.')
    parser.add_argument('folder', type=str, help='The folder to search in.')
    parser.add_argument('file_prefix', type=str, help='The filename prefix to search for.')

    args = parser.parse_args()

    find_duplicates(args.folder, args.file_prefix)
