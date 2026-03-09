from pathlib import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # Validates that target directory falls within the working directory
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir) == False:
            return f'Error: "{directory}" is not a directory'

        # Build file info text block
        files_info = []
        for filename in os.listdir(target_dir):
            full_filepath = os.path.normpath(os.path.join(target_dir, filename))
            is_dir = os.path.isdir(full_filepath)
            file_size = os.path.getsize(full_filepath)
            files_info.append(
                f"- {filename}: file_size={file_size} bytes, is_dir={is_dir}"
            )
        return "\n".join(files_info)
    except Exception as e:
        return f"Error listing files: {e}"
