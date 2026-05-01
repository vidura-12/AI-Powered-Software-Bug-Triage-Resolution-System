# tools/tool2_read_code.py

def read_code_file_tool(path: str) -> str:
    """
    Reads a local Python or JavaScript source code file and returns
    its content with line numbers prepended to each line.

    This tool is used by the Code Analyser Agent to inspect source
    files and identify potential root causes of reported bugs.

    Args:
        path (str): The absolute or relative file path to the source
                    code file (.py or .js) to be read.

    Returns:
        str: The full content of the file with line numbers in the
             format "  1 | <code line>". Returns an error message
             string if the file cannot be found or read.

    Example:
        >>> content = read_code_file_tool("sample_code/buggy_app.py")
        >>> print(content[:100])
          1 | def divide(a, b):
          2 |     return a / b
    """
    supported_extensions = (".py", ".js", ".ts", ".jsx", ".tsx")

    # Validate file extension
    if not path.endswith(supported_extensions):
        return (
            f"ERROR: Unsupported file type. "
            f"Only {supported_extensions} files are supported."
        )

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Add line numbers to each line
        numbered_lines = []
        for i, line in enumerate(lines, start=1):
            numbered_lines.append(f"{i:>4} | {line}")

        return "".join(numbered_lines)

    except FileNotFoundError:
        return f"ERROR: File not found at path: '{path}'"
    except PermissionError:
        return f"ERROR: Permission denied when reading file: '{path}'"
    except Exception as e:
        return f"ERROR: Unexpected error reading file: {str(e)}"