import os

def write_report(output_path: str, content: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n✅ Report successfully saved at: {output_path}")