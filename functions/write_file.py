import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites a file with the provided content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to overwrite",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to overwrite the file with",
            ),
        },
    ),
)


def write_file(working_directory: str, file_path: str, content: str):
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(
        os.path.join(os.path.abspath(working_directory), file_path)
    )

    if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    try:
        os.makedirs(os.path.dirname(target_path), exist_ok=True)

        with open(target_path, "w") as f:
            f.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"
