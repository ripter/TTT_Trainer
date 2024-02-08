import os

def get_unique_filename(base_filename):
    counter = 1
    filename, extension = os.path.splitext(base_filename)
    unique_filename = f"{filename}{counter}{extension}"
    while os.path.exists(unique_filename):
        counter += 1
        unique_filename = f"{filename}{counter}{extension}"

    return unique_filename