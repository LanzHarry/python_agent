import os

from openai.types.chat import ChatCompletionToolParam

schema_write_file: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes string of content to a specified file_path (relative to the working directory). If the file or its parent directories don't exist they will be created.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of the file to write to. The file path is relative to the working directory.",
                },
                "content": {
                    "type": "string",
                    "description": "The string of content to be written to the specified file.",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}


def write_file(working_dir: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs_path = os.path.abspath(working_dir)
        file_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
        valid_file_path = (
            os.path.commonpath([working_dir_abs_path, file_path])
            == working_dir_abs_path
        )
        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        file_parent_dir_abs_path = os.path.split(file_path)[0]

        os.makedirs(name=file_parent_dir_abs_path, exist_ok=True)

        with open(file_path, "w") as file_to_write:
            _ = file_to_write.write(content)

        return f'Successfully wrote to file "{file_path}" ({len(content)} characters written)'

    except (OSError, ValueError) as e:
        return f"Error: {e}"
