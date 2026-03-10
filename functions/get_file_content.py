from pathlib import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        # Validates that target directory falls within the working directory
        # print(f"Full file path -> {abs_file_path}")
        # print(f"Full working dir -> {abs_working_dir}")
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if os.path.isfile(abs_file_path) == False:
            return f'Error: "{file_path}" is not a file'

        # Open and read file. Truncate if too long.
        with open(abs_file_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        
        return content

    except Exception as e:
        return f"Error: reading file: {e}"
