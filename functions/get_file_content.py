import os

from openai.types.chat import ChatCompletionToolParam

from config import MAX_CHARS_TO_READ

schema_get_file_content: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns the contents of a file (as a string) up to a pre-defined maximum character limit",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path of the file to get content from. The file path is relative to the working directory.",
                },
            },
            "required": ["file_path"],
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
        file_path = os.path.normpath(os.path.join(working_dir_abs_path, file_path))
        valid_file_path = (
            os.path.commonpath([working_dir_abs_path, file_path])
            == working_dir_abs_path
        )
        if not valid_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS_TO_READ)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS_TO_READ} characters]'

        return file_content_string

    except (OSError, ValueError) as e:
        return f"Error: {e}"
