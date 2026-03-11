from pathlib import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes specificed text data to file at specified file path. File will be created automatically if needed. If the file already exsists, the data will be overwritten.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to file relative to the working directory. If the file is at the root of the working directory only the file name needs to be given",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Text string to be written to the file",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        # Validates that target directory falls within the working directory
        # print(f"Full file path -> {abs_file_path}")
        # print(f"Full working dir -> {abs_working_dir}")
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        abs_parent_dir = os.path.dirname(abs_file_path)
        # print(f"Parent Dir -> {abs_parent_dir}")
        os.makedirs(abs_parent_dir, exist_ok=True)

        with open(abs_file_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    
    except Exception as e:
        return f"Error: writing to file: {e}"

