import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs_path = os.path.abspath(working_directory)
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

        return f'Successfully wrote to file "{file_path}" ({len(content)} characters writter)'

    except (OSError, ValueError) as e:
        return f"Error: {e}"
