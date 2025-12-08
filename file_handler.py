import yaml 
from pathlib import Path 
from datetime import datetime

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

def write_to_text_file(updated_cv, config):
    print("Writing to text files...")
    folder_name = updated_cv.get("job_application_business_name") or datetime.today().strftime("%Y-%m-%d%H%M")
    folder_path = Path(config["output_folder"], folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)

    with open(folder_path / config["job_experience_file"], "w", encoding="utf-8") as f:
        f.write(updated_cv["job_experience"])
    print(f"Writing to {config["job_experience_file"]} SUCESS!")

    with open(folder_path / config["skills_file"], "w", encoding="utf-8") as f:
        f.write(updated_cv["skills"])
    print(f"Writing to {config["skills_file"]} SUCESS!")
    
    with open(folder_path / config["suggested_skills_file"], "w", encoding="utf-8") as f:
        f.write("\n".join(updated_cv["suggested_skills"]))
    print(f"Writing to {config["suggested_skills_file"]} SUCESS!")