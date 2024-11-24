import os
from pathlib import Path

def execute_task1():
    base_dir = Path().resolve()
    print(f"Current directory: {base_dir}")
    target_dir = base_dir / 'Example_Files'
    print(f"Searching in directory: {target_dir}")

    image_file = next(target_dir.glob('*.png'), None)
    doc_file = next(target_dir.glob('*.docx'), None)

    if image_file:
        print(f"Found image file: {image_file}")
        os.startfile(image_file)
    if doc_file:
        print(f"Found document file: {doc_file}")
        os.startfile(doc_file)

if __name__ == '__main__':
    execute_task1()
