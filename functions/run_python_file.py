import os
import subprocess
from typing import Any

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file with optional arguments and returns it's exit code, stdout and stderr",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the python file to run",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="An optional array of arguments to pass to the python file",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)


def run_python_file(
    working_directory: str, file_path: str, args: list[Any] | None = None
):
    working_dir_abs = os.path.abspath(working_directory)
    absolute_file_path = os.path.normpath(
        os.path.join(os.path.abspath(working_directory), file_path)
    )

    if os.path.commonpath([working_dir_abs, absolute_file_path]) != working_dir_abs:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(absolute_file_path):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    if not absolute_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", absolute_file_path]
    if args:
        command.extend(args)

    try:
        result = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = ""

        if result.returncode != 0:
            output += f"Process exited with {result.returncode}\n"

        if not result.stdout and not result.stderr:
            output += "No output produced\n"
        else:
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}"

            if result.stderr:
                output += f"STDERR:\n{result.stderr}"

        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
