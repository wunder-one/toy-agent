from pathlib import os

def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        # Validates that target directory falls within the working directory
        # print(f"Full file path -> {abs_file_path}")
        # print(f"Full working dir -> {abs_working_dir}")
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(abs_file_path) == True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        abs_parent_dir = os.path.dirname(abs_file_path)
        # print(f"Parent Dir -> {abs_parent_dir}")
        os.makedirs(abs_parent_dir, exist_ok=True)

        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    
    except Exception as e:
        return f"Error: reading file: {e}"

