# tools/read_bug_report_tool.py

def read_bug_report(file_path: str) -> str:
    """
    Reads a plain text or JSON bug report file from the local filesystem
    and returns its contents as a string.

    Args:
        file_path (str): The absolute or relative path to the bug report file.
                         Supports .txt and .json formats.

    Returns:
        str: The full text content of the bug report.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
        ValueError: If the file format is not .txt or .json.
    """
    import os
    import json

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Bug report not found at path: {file_path}")

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    elif ext == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Flatten JSON to readable string for the LLM
            return json.dumps(data, indent=2)

    else:
        raise ValueError(f"Unsupported file format '{ext}'. Use .txt or .json.")