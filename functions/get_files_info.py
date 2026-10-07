import os

from openai.types.chat import ChatCompletionToolParam

schema_get_files_info: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "target_dir_rel": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_dir: str, target_dir_rel: str) -> str:
    try:
        working_dir_abs_path = os.path.abspath(working_dir)
        target_dir = os.path.normpath(
            os.path.join(working_dir_abs_path, target_dir_rel)
        )
        valid_target_dir = (
            os.path.commonpath([working_dir_abs_path, target_dir])
            == working_dir_abs_path
        )
        if not valid_target_dir:
            return f'Error: Cannot list "{target_dir_rel}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{target_dir_rel}" is not a directory'

        return_string = ""
        dir_contents = os.listdir(target_dir)

        for elt in dir_contents:
            abs_elt_path = os.path.join(target_dir, elt)
            return_string += f"- {elt}: file_size={os.path.getsize(abs_elt_path)} bytes, is_dir={os.path.isdir(abs_elt_path)}\n"

        return return_string

    except (OSError, ValueError) as e:
        return f"Error: {e}"
