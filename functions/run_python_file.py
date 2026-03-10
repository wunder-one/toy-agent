from pathlib import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        # Validates that target directory falls within the working directory
        print("Validating python file...")
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if abs_file_path[-2:] != "py":
            return f'Error: "{file_path}" is not a Python file'

        # Execute python file
        print("Executing python file...")
        command = ["python", abs_file_path]
        if args:
            command.extend(args)
        # print(f"Command is: {command}")
        result = subprocess.run(
            command, 
            cwd=abs_working_dir, 
            capture_output=True, 
            text=True, 
            timeout=30,
        )

        # Build output string
        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT: {result.stdout}")
        if result.stderr:
            output.append(f"STDERR: {result.stderr}")

        return "\n".join(output)
        

    except Exception as e:
        return f"Error: writing to file: {e}"