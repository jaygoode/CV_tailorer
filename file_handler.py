import json
from datetime import datetime
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()


def write_json_file(data: dict, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def read_json_file(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def read_yaml_file(filepath: str) -> dict:
    """
    Read and parse a YAML file.

    Args:
        filepath (str): Path to the YAML file.

    Returns:
        dict: Parsed YAML data.
    """

    with open(filepath, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def read_txt_file(filepath: str):
    """
    Read a plain text (.txt) file.

    Args:
        filepath (str): Path to the text file.

    Returns:
        str: File contents as a string.
    """

    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def create_text_files(updated_cv: dict, config: dict) -> Path:
    print("Writing to text files...")
    folder_name = updated_cv.get(
        "job_application_business_name"
    ) or datetime.today().strftime("%Y-%m-%d%H%M")
    folder_path = Path(config["output_folder"], folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)

    file_topics = list(updated_cv.keys())
    for file_topic in file_topics:
        with open(
            (folder_path / file_topic).with_suffix(".txt"), "w", encoding="utf-8"
        ) as f:
            if isinstance(updated_cv[file_topic], list):
                f.write("\n".join(updated_cv[file_topic]))
                continue
            f.write(updated_cv[file_topic])
        print(f"Writing {file_topic} SUCCESS!")

    return folder_path
