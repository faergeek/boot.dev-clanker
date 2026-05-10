import os

from google.genai import types

from config import MAX_CHARS

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads the specified file and returns it's content truncated to the maximum of {MAX_CHARS} characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory",
            )
        },
    ),
)


def get_file_content(working_directory: str, file_path: str):
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(
        os.path.join(os.path.abspath(working_directory), file_path)
    )

    if os.path.commonpath([working_dir_abs, target_path]) != working_dir_abs:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(target_path) as f:
            content = f.read(MAX_CHARS)

            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS}]'

            return content
    except Exception as e:
        return f"Error: {e}"
