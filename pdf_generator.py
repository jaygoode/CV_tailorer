from dotenv import load_dotenv
import os
from fpdf import FPDF
import re
from pathlib import Path 

load_dotenv()

#LINE HEIGHT AND WIDTH SETTINGS
HEADER_LINE_HEIGHT = 13
SUB_HEADER_LINE_HEIGHT = 7.5
LINE_HEIGHT = 5
LINE_WIDTH = 0

#FONT SETTINGS
MAIN_HEADER_FONT_SIZE = 14
SUB_HEADER_FONT_SIZE = 12
PARAGRAPH_FONT_SIZE = 11
FONT = "DejaVu"
# FONT = "Arial"
MARGIN = 10

#profile image settings
IMG_WIDTH = 28  
IMG_HEIGHT = 38  
X_START = MARGIN
Y_START = MARGIN

def generate_cv_pdf(updated_cv_data: dict, cv_data: dict, profile_picture_path: str, folder_path: Path):
    """
    Generates a simple, ATS-friendly CV PDF from structured CV data.

    Parameters:
    - cv_data: dict with keys like 'name', 'cv_job_experience', 'cv_skills', 'key_achievements'
    """
    cleaned_updated_cv_data=sanitize_text(updated_cv_data)
    cleaned_cv_data=sanitize_text(cv_data)
    pdf = FPDF()

   
    pdf.add_font(FONT, "", "fonts/DejaVuSans.ttf", uni=True)
    pdf.add_font(FONT, "B", "fonts/DejaVuSans-Bold.ttf", uni=True)  # Bold

    pdf.set_font(FONT, size=12)

    pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.set_auto_page_break(auto=True, margin=MARGIN)
    pdf.add_page()
    
    create_pdf_header(pdf, cleaned_cv_data, profile_picture_path)
    draw_horizontal_separator(pdf)
    create_experience_section(pdf, cleaned_updated_cv_data)
    create_skills_section(pdf, cleaned_updated_cv_data)
    create_achievements_section(pdf, cleaned_updated_cv_data)
    create_pdf_file(pdf, folder_path)

def create_pdf_header(pdf: FPDF, cleaned_cv_data, profile_picture_path: str):
    header_data = {
    "location": os.getenv("LOCATION"),
    "languages": cleaned_cv_data["languages"],
    "email_and_phone": os.getenv("EMAIL_PHONE"),
    "linkedin": os.getenv("LINKEDIN"),
    "github": os.getenv("GITHUB")
}
    # add_profile_image(pdf, profile_picture_path)
    pdf.image(profile_picture_path, x=X_START, y=Y_START, w=IMG_WIDTH, h=IMG_HEIGHT)

    #SETTING NAME 
    pdf.set_x(X_START + IMG_WIDTH + 5)  # 5mm space after image
    pdf.set_font(FONT, "B", MAIN_HEADER_FONT_SIZE)  
    pdf.cell(LINE_WIDTH, LINE_HEIGHT, os.getenv("NAME"), ln=True)  

    #SETTING ROLE 
    pdf.set_x(X_START + IMG_WIDTH + 5)  # 5mm space after image
    pdf.set_font(FONT, "", SUB_HEADER_FONT_SIZE + 2)  
    pdf.cell(LINE_WIDTH, SUB_HEADER_LINE_HEIGHT, cleaned_cv_data["role"], ln=True)  #cell(width, height, text, ln=True moves cursor to next line)
    
    #SETTING CONTACT INFO
    pdf.set_font(FONT, "", PARAGRAPH_FONT_SIZE)  
    for value in header_data.values():
        pdf.set_x(X_START + IMG_WIDTH + 5)  # 5mm space after image
        pdf.cell(LINE_WIDTH, LINE_HEIGHT, value, ln=True)

def create_experience_section(pdf: FPDF, cleaned_updated_cv_data: dict):
    pdf.set_x(MARGIN)
    pdf.set_font(FONT, "B", MAIN_HEADER_FONT_SIZE)       
    pdf.cell(LINE_WIDTH, HEADER_LINE_HEIGHT, "PROFESSIONAL EXPERIENCE", ln=True)
    pdf.set_font(FONT, "", PARAGRAPH_FONT_SIZE) 
    
    #split on double newlines to get separate experience sections
    sections_experience_text = re.split(r"\n\s*\n", cleaned_updated_cv_data["cv_job_experience"].strip())
    for section in sections_experience_text:
        split_experience_text = section.split('\n')
        for i, line in enumerate(split_experience_text):
            pdf.set_x(MARGIN)
            if i == 0 or i == 1:
                pdf.set_font(FONT, "B", PARAGRAPH_FONT_SIZE)
                pdf.multi_cell(LINE_WIDTH, SUB_HEADER_LINE_HEIGHT-1.5, line.strip())
            else:
                pdf.set_x(MARGIN+5)
                pdf.set_font(FONT, "", PARAGRAPH_FONT_SIZE)
                pdf.multi_cell(LINE_WIDTH, LINE_HEIGHT, line.strip())

def create_skills_section(pdf:FPDF, cleaned_updated_cv_data:dict):
    pdf.set_x(MARGIN)
    pdf.set_font(FONT, "B", MAIN_HEADER_FONT_SIZE)
    pdf.cell(LINE_WIDTH, HEADER_LINE_HEIGHT, "SKILLS", ln=True)
    pdf.set_font(FONT, "", PARAGRAPH_FONT_SIZE)
    pdf.multi_cell(LINE_WIDTH, LINE_HEIGHT, cleaned_updated_cv_data["skills"])
    
def create_achievements_section(pdf, cleaned_updated_cv_data):
    pdf.set_x(MARGIN)
    pdf.set_font(FONT, "B", MAIN_HEADER_FONT_SIZE)
    pdf.cell(LINE_WIDTH, HEADER_LINE_HEIGHT, "KEY ACHIEVEMENTS", ln=True)
    pdf.set_font(FONT, "", PARAGRAPH_FONT_SIZE)
    pdf.multi_cell(LINE_WIDTH, LINE_HEIGHT, cleaned_updated_cv_data.get("key_achievements", ""))

def create_pdf_file(pdf:FPDF, folder_path: Path):
    filepath = folder_path / "Johnny_nylund_CV.pdf"
    filename = str(filepath)
    pdf.output(filename)
    print(f"CV successfully generated: {filename}")


def sanitize_text(obj):
    """
    Recursively replace Unicode bullets and en dashes with ASCII equivalents
    in strings, lists, or dicts.
    """
    if isinstance(obj, str):
        obj = obj.replace("–", "-").replace("  ", "")
        # obj = obj.replace("•", "-").replace("–", "-").replace("  ", "")
        return obj
    elif isinstance(obj, list):
        return [sanitize_text(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: sanitize_text(value) for key, value in obj.items()}
    else:
        return obj  

# def create_bulletpoints_section(pdf:FPDF, cleaned_updated_cv_data, cv_data_section:str):
#     pdf.set_font(FONT, "B", PARAGRAPH_FONT_SIZE)
#     bullet_points = cleaned_updated_cv_data.get(cv_data_section)
#     #might have to split strings at bulletpoint characters.
#     if isinstance(bullet_points, list):
#         for point in bullet_points:
#             pdf.cell(LINE_WIDTH, LINE_HEIGHT, point, ln=True)
#     else:
#         pdf.cell(LINE_WIDTH, LINE_HEIGHT, point, ln=True)

def draw_horizontal_separator(pdf: FPDF):
    y = pdf.get_y() + 2  # small vertical spacing after header
    pdf.line(
        MARGIN,
        y,
        pdf.w - MARGIN,
        y
    )
    pdf.ln(6)  # space after the line