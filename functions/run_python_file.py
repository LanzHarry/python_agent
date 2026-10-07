import os
import subprocess
from openai.types.chat import ChatCompletionToolParam

schema_run_python_file: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs the python file at the specified file path (relative to the working directory). If the file requires arguments they can also be provided as a list of strings.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of the python file to run. The file path is relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Argument list to be provided to the python file. These arguments are optional and will be appended to the command that runs the python file if present.",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
        valid_file_path = (
            os.path.commonpath([working_dir_abs_path, file_path_abs])
            == working_dir_abs_path
        )
        if not valid_file_path:
            return f'Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path_abs):
            return f'"{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_path_abs]

        if args is not None:
            command.extend(args)

        timeout_len_seconds = 30

        process_result = subprocess.run(
            command,
            cwd=working_dir_abs_path,
            capture_output=True,
            text=True,
            timeout=timeout_len_seconds,
        )

        output_string = ""

        if process_result.returncode != 0:
            output_string += f"Process exited with code {process_result.returncode}\n"

        if not process_result.stdout and not process_result.stderr:
            output_string += "No output produced"

        if process_result.stdout:
            output_string += f"STDOUT: {process_result.stdout}"

        if process_result.stderr:
            output_string += f"STDERR: {process_result.stderr}"

        return output_string

    except (IOError, ValueError) as e:
        return f"Error: {e}"
