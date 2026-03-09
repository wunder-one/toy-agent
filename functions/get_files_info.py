from pathlib import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # Validates that target directory falls within the working directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        #print(f"Working Dir: {working_dir_abs}")
        #print(f"Targer Dir Exsists: {os.path.exists(target_dir)}")
        #print(f"Is Valid: {valid_target_dir}")
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if os.path.exists(target_dir) == False:
            return f'Error: "{directory}" is not a directory'

        target_dir_contents = os.listdir(target_dir)

        # Build file info text block
        files_info = ""
        for filename in target_dir_contents:
            full_filepath = os.path.normpath(os.path.join(target_dir, filename))
            files_info = f"{files_info}\n{filename}: file_size={os.path.getsize(full_filepath)} bytes, is_dir={os.path.isdir(full_filepath)}"
        return files_info[1:]
    except Exception as e:
        print(f"Error: Unable to verify local file directories: {e}")    