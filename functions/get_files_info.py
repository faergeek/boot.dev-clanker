import os


def get_files_info(working_directory: str, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(
        os.path.join(os.path.abspath(working_directory), directory)
    )
    if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        return "\n".join(
            f"- {entry.name}: file_size={entry.stat().st_size} bytes, is_dir={os.path.isdir(entry.path)}"
            for entry in os.scandir(target_dir)
        )
    except Exception as e:
        return f"Error: {e}"
