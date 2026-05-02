def write_report(file_path: str, content: str) -> None:
    """
    Writes the generated bug report to a file.

    Args:
        file_path (str): The destination file path where the report will be saved.
        content (str): The full bug report content.

    Raises:
        IOError: If the file cannot be written.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print(f"✅ Report successfully saved at: {file_path}")
    except Exception as e:
        print(f"❌ Error writing report: {e}")