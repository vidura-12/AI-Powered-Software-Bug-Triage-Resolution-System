# tools/search_local_docs_tool.py

def search_local_docs(query: str, search_path: str = ".") -> list[str]:
    """
    Searches local source code files for lines that match a given query string.

    This tool scans Python, JavaScript, and TypeScript files in the project
    directory and returns relevant lines that may help identify code patterns
    or fixes.

    Args:
        query (str): Keyword or pattern to search for (e.g., error message, function name).
        search_path (str): Root directory to search in (default is current project).

    Returns:
        list[str]: A list of matching lines with file names and line numbers.

    Raises:
        ValueError: If the query string is empty.
    """
    import os
    import re

    if not query or not query.strip():
        raise ValueError("Search query cannot be empty.")

    results = []

    for root, _, files in os.walk(search_path):
        for file in files:
            if file.endswith((".py", ".js", ".ts")):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()

                        for i, line in enumerate(lines):
                            if re.search(query, line, re.IGNORECASE):
                                results.append(
                                    f"{file_path} (line {i+1}): {line.strip()}"
                                )

                except Exception:
                    # Skip unreadable files safely
                    continue

    return results[:10]  # limit output for LLM efficiency