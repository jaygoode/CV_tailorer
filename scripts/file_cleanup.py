import shutil
from pathlib import Path


def cleanup_files():
    print("Starting file cleanup...")
    input_folder = Path("input_files/")
    output_folder = Path("output_files/")

    for file in input_folder.iterdir():
        if file.is_file() and file.suffix == ".txt":
            file.unlink()
            print(f"Deleted file: {file.name}")

    for folder in output_folder.iterdir():
        if folder.is_dir():
            shutil.rmtree(folder)
            print(f"Deleted folder: {folder.name}")
    print("File cleanup completed.")
