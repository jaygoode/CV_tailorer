import yaml 
from pathlib import Path 
from datetime import datetime
from dotenv import load_dotenv
import os
from fpdf import FPDF
import json

load_dotenv()

def write_json_file(data: dict, filepath: str):
    with open(filepath, "w", encoding="utf-8") as f:
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

def create_text_files(updated_cv:dict, config:dict):
    print("Writing to text files...")
    folder_name = updated_cv.get("job_application_business_name") or datetime.today().strftime("%Y-%m-%d%H%M")
    folder_path = Path(config["output_folder"], folder_name)
    folder_path.mkdir(parents=True, exist_ok=True)


    file_topics = list(updated_cv.keys())
    for file_topic in file_topics:
        with open((folder_path / file_topic).with_suffix(".txt"), "w", encoding="utf-8") as f:
            if isinstance(updated_cv[file_topic], list):
                    f.write("\n".join(updated_cv[file_topic]))
                    continue
            f.write(updated_cv[file_topic])
        print(f"Writing {file_topic} SUCCESS!")


header_line_height = 8
line_height = 5
line_width = 0
main_header_font_size = 16
sub_header_font_size = 13
paragraph_font_size = 11.5
font="Arial"

def generate_cv_pdf(updated_cv_data: dict, cv_data: dict, profile_picture_path: str ):
    """
    Generates a simple, ATS-friendly CV PDF from structured CV data.

    Parameters:
    - cv_data: dict with keys like 'name', 'cv_job_experience', 'cv_skills', 'key_achievements'
    """
    cleaned_updated_cv_data=sanitize_text(updated_cv_data)
    cleaned_cv_data=sanitize_text(cv_data)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()
    
    generate_pdf_header(pdf, cleaned_cv_data, profile_picture_path)

    pdf.set_font(font, "B", main_header_font_size)       # Bold font for section title
    pdf.cell(0, header_line_height, "Experience:", ln=True)
    
    pdf.set_font(font, "", sub_header_font_size)        # Regular font for content
    pdf.multi_cell(0, 8, cleaned_updated_cv_data.get("cv_job_experience", ""))  
    # multi_cell(width, height, text) wraps text to the next line if it's too long
    # width=0 makes it fill the page width

    # -------------------------
    # Skills section
    # -------------------------
    pdf.set_font(font, "B", sub_header_font_size)
    pdf.cell(line_width, header_line_height, "Skills:", ln=True)
    create_skills_section(pdf, cleaned_updated_cv_data)
    
    # -------------------------
    # Achievements section
    # -------------------------
    pdf.set_font(font, "B", sub_header_font_size)
    pdf.cell(0, header_line_height, "Key Achievements:", ln=True)
    
    pdf.set_font(font, "", sub_header_font_size)
    pdf.multi_cell(0, 8, cleaned_updated_cv_data.get("key_achievements", ""))

    create_pdf_file(pdf)

def create_pdf_file(pdf):
    filename="cv.pdf"
    pdf.output(filename)
    print(f"CV successfully generated: {filename}")

def generate_pdf_header(pdf: FPDF, cleaned_cv_data, profile_picture_path: str):
    name = os.getenv("NAME") 
    email_and_phone = os.getenv("EMAIL_PHONE") 
    location = os.getenv("LOCATION") 
    linkedin = os.getenv("LINKEDIN") 
    github = os.getenv("GITHUB") 

    # add_profile_image(pdf, profile_picture_path)
    pdf.set_font(font, "B", main_header_font_size)  
    pdf.cell(line_width, header_line_height, name, ln=True)  
    pdf.set_font(font, "", main_header_font_size)  
    pdf.cell(line_width, header_line_height, cleaned_cv_data["role"], ln=True)  #cell(width, height, text, ln=True moves cursor to next line)
    pdf.set_font(font, "", paragraph_font_size)  
    pdf.cell(line_width, line_height, location, ln=True)
    pdf.cell(line_width, line_height, cleaned_cv_data["languages"], ln=True) 
    pdf.cell(line_width, line_height, email_and_phone, ln=True)  
    pdf.cell(line_width, line_height, linkedin, ln=True)  
    pdf.cell(line_width, line_height, github, ln=True) 

def add_profile_image(pdf: FPDF, profile_picture_path: str):
    img_width = 30  
    img_height = 30  
    x_start = line_height
    y_start = line_height
    pdf.image(profile_picture_path, x=x_start, y=y_start, w=img_width, h=img_height)
    # Move cursor to the right of the image
    pdf.set_xy(x_start + img_width + 5, y_start)  # 5mm space after image

def sanitize_text(obj):
    """
    Recursively replace Unicode bullets and en dashes with ASCII equivalents
    in strings, lists, or dicts.
    """
    if isinstance(obj, str):
        return obj.replace("•", "-").replace("–", "-")
    elif isinstance(obj, list):
        return [sanitize_text(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: sanitize_text(value) for key, value in obj.items()}
    else:
        return obj  

def create_skills_section(pdf:FPDF, cleaned_updated_cv_data:dict):

    skills = cleaned_updated_cv_data.get("cv_skills", [])
    if isinstance(skills, list):
        # Join list items with line breaks
        pdf.cell(line_width, 8, "\n".join(skills))
    else:
        pdf.cell(line_width, 8, skills)

def create_bulletpoints_section(pdf:FPDF, cleaned_updated_cv_data, cv_data_section:str):
    pdf.set_font(font, "B", paragraph_font_size)
    bullet_points = cleaned_updated_cv_data.get(cv_data_section)
    #might have to split strings at bulletpoint characters.
    if isinstance(bullet_points, list):
        for point in bullet_points:
            pdf.cell(line_width, line_height, point, ln=True)
    else:
        pdf.cell(line_width, line_height, point, ln=True)