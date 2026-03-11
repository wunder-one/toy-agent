from pathlib import os
from google.genai import types
from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Fetch contents of specified file. Returned data is limited to {MAX_CHARS} characters to save on tokens",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to file relative to the working directory. If the file is at the root of the working directory only the file name needs to be given",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        # Validates that target directory falls within the working directory
        # print(f"Full file path -> {abs_file_path}")
        # print(f"Full working dir -> {abs_working_dir}")
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
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
