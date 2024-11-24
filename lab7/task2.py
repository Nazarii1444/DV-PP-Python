from pathlib import Path
import subprocess

def run_files_with_editor():
    working_dir = Path().resolve()
    print(f"Base folder: {working_dir}")
    target_folder = working_dir / "Documents"

    txt_files = list(target_folder.glob('*.txt'))
    print(f"Text files found: {txt_files}")

    editor_path = r"C:\Program Files\Notepad++\notepad++.exe"

    if txt_files:
        file_paths = [str(file) for file in txt_files]
        print(f"Opening files with editor: {editor_path}")
        subprocess.Popen([editor_path] + file_paths)  # Використовуємо Popen для запуску
    else:
        print("No text files found to open.")

if __name__ == '__main__':
    run_files_with_editor()
