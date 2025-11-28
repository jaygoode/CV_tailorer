import yaml 
from pathlib import Path 

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

def read_txt_file(filepath:str):
    """
    Read a plain text (.txt) file.

    Args:
        filepath (str): Path to the text file.

    Returns:
        str: File contents as a string.
    """

    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()

def write_to_text_file(updated_cv):
    print("Writing to text files...")
    folder_path = Path("./output_file", updated_cv["job_application_business_name"])
    folder_path.mkdir(parents=True, exist_ok=True)

    with open(f"{folder_path}/job_experience_text.txt", "w", encoding="utf-8") as f:
        f.write(updated_cv["job_experience"])
    print("Writing to job_experience_text.txt SUCCESS!")

    with open(f"{folder_path}/skills_text.txt", "w", encoding="utf-8") as f:
        f.write(updated_cv["skills"])
    print("Writing to skills_text.txt SUCESS!")