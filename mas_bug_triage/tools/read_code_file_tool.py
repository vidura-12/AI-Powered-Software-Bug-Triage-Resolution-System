# tools/read_code_file_tool.py

import os


def read_code_file(path: str) -> str:
    """
    Reads a local Python or JavaScript source code file and returns
    its content with line numbers prepended to each line.

    This tool is used by the Code Analyser Agent to inspect source
    files and identify potential root causes of reported bugs.

    Args:
        path (str): The absolute or relative file path to the source
                    code file. Supports .py, .js, .ts, .jsx, .tsx

    Returns:
        str: The full content of the file with line numbers in the
             format "   1 | <code line>". Returns an error message
             string if the file cannot be found or read.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
        ValueError: If the file extension is not supported.

    Example:
        >>> content = read_code_file("sample_code/buggy_app.py")
        >>> print(content)
           1 | def divide(a, b):
           2 |     return a / b
    """
    supported_extensions = (".py", ".js", ".ts", ".jsx", ".tsx")

    # --- Validate file exists ---
    if not os.path.exists(path):
        raise FileNotFoundError(f"Source file not found at path: '{path}'")

    # --- Validate file extension ---
    ext = os.path.splitext(path)[1].lower()
    if ext not in supported_extensions:
        raise ValueError(
            f"Unsupported file type '{ext}'. "
            f"Supported types: {supported_extensions}"
        )

    # --- Read and number each line ---
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        numbered_lines = [f"{i:>4} | {line}" for i, line in enumerate(lines, 1)]
        return "".join(numbered_lines)

    except PermissionError:
        raise PermissionError(f"Permission denied when reading file: '{path}'")
    except Exception as e:
        raise RuntimeError(f"Unexpected error reading file '{path}': {str(e)}")