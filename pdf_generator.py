from dotenv import load_dotenv
import os
from fpdf import FPDF

load_dotenv()

HEADER_LINE_HEIGHT = 15
SUB_HEADER_LINE_HEIGHT = 8
LINE_HEIGHT = 5
LINE_WIDTH = 0
MAIN_HEADER_FONT_SIZE = 16
SUB_HEADER_FONT_SIZE = 13
PARAGRAPH_FONT_SIZE = 11.5
FONT = "Arial"
MARGIN = 10

def generate_cv_pdf(updated_cv_data: dict, cv_data: dict, profile_picture_path: str):
    """
    Generates a simple, ATS-friendly CV PDF from structured CV data.

    Parameters:
    - cv_data: dict with keys like 'name', 'cv_job_experience', 'cv_skills', 'key_achievements'
    """
    cleaned_updated_cv_data=sanitize_text(updated_cv_data)
    cleaned_cv_data=sanitize_text(cv_data)
    pdf = FPDF()
    pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.set_auto_page_break(auto=True, margin=MARGIN)
    pdf.add_page()
    
    create_pdf_header(pdf, cleaned_cv_data, profile_picture_path)
    draw_horizontal_separator(pdf)
    create_experience_section(pdf, cleaned_updated_cv_data)
    create_skills_section(pdf, cleaned_updated_cv_data)
    create_achievements_section(pdf, cleaned_updated_cv_data)
    create_pdf_file(pdf)

def create_pdf_header(pdf: FPDF, cleaned_cv_data, profile_picture_path: str):
    header_data = {
    "location": os.getenv("LOCATION"),
    "languages": cleaned_cv_data["languages"],
    "email_and_phone": os.getenv("EMAIL_PHONE"),
    "linkedin": os.getenv("LINKEDIN"),
    "github": os.getenv("GITHUB")
}
    # add_profile_image(pdf, profile_picture_path)
    pdf.set_font(FONT, "B", MAIN_HEADER_FONT_SIZE)  
    pdf.cell(LINE_WIDTH, SUB_HEADER_LINE_HEIGHT, os.getenv("NAME"), ln=True)  
    pdf.set_font(FONT, "", MAIN_HEADER_FONT_SIZE)  
    pdf.cell(LINE_WIDTH, SUB_HEADER_LINE_HEIGHT, cleaned_cv_data["role"], ln=True)  #cell(width, height, text, ln=True moves cursor to next line)
    
    pdf.set_font(FONT, "", PARAGRAPH_FONT_SIZE)  
    for value in header_data.values():
        pdf.cell(LINE_WIDTH, LINE_HEIGHT, value, ln=True)

def create_experience_section(pdf: FPDF, cleaned_updated_cv_data: dict):
    #can we split if line starts with dash? or split on newline and grab 2 first lines for subheaders?
    #what happens if ai doesnt create correct format?
    pdf.set_x(MARGIN)
    pdf.set_font(FONT, "B", MAIN_HEADER_FONT_SIZE)       
    pdf.cell(LINE_WIDTH, HEADER_LINE_HEIGHT, "PROFESSIONAL EXPERIENCE", ln=True)
    pdf.set_font(FONT, "", PARAGRAPH_FONT_SIZE) 
    # pdf.set_x(MARGIN)
    pdf.multi_cell(LINE_WIDTH, LINE_HEIGHT, cleaned_updated_cv_data["cv_job_experience"])  

def create_skills_section(pdf:FPDF, cleaned_updated_cv_data:dict):
    pdf.set_x(MARGIN)
    pdf.set_font(FONT, "B", SUB_HEADER_FONT_SIZE)
    pdf.cell(LINE_WIDTH, HEADER_LINE_HEIGHT, "SKILLS", ln=True)
    pdf.set_font(FONT, "", PARAGRAPH_FONT_SIZE)
    pdf.multi_cell(LINE_WIDTH, LINE_HEIGHT, cleaned_updated_cv_data["skills"])
    # if isinstance(skills, list):
    #     pdf.cell(LINE_WIDTH, LINE_HEIGHT, "\n".join(skills))
    # else:
    #     pdf.cell(LINE_WIDTH, LINE_HEIGHT, skills)
    
def create_achievements_section(pdf, cleaned_updated_cv_data):
    pdf.set_x(MARGIN)
    pdf.set_font(FONT, "B", MAIN_HEADER_FONT_SIZE)
    pdf.cell(LINE_WIDTH, HEADER_LINE_HEIGHT, "KEY ACHIEVEMENTS", ln=True)
    pdf.set_font(FONT, "", PARAGRAPH_FONT_SIZE)
    pdf.multi_cell(LINE_WIDTH, LINE_HEIGHT, cleaned_updated_cv_data.get("key_achievements", ""))

def create_pdf_file(pdf):
    filename="cv.pdf"
    pdf.output(filename)
    print(f"CV successfully generated: {filename}")


def add_profile_image(pdf: FPDF, profile_picture_path: str):
    img_width = 30  
    img_height = 30  
    x_start = LINE_HEIGHT
    y_start = LINE_HEIGHT
    pdf.image(profile_picture_path, x=x_start, y=y_start, w=img_width, h=img_height)
    # Move cursor to the right of the image
    pdf.set_xy(x_start + img_width + 5, y_start)  # 5mm space after image

def sanitize_text(obj):
    """
    Recursively replace Unicode bullets and en dashes with ASCII equivalents
    in strings, lists, or dicts.
    """
    if isinstance(obj, str):
        return obj.replace("•", "-").replace("–", "-").replace("  ", "")
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