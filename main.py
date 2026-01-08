# from langchain_community.chat_models import ChatOllama
from pathlib import Path
from pprint import pprint

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

import file_handler
import pdf_generator


class CVText(BaseModel):
    professional_summary: str = Field(
        ..., description="The improved CV professional summary text."
    )
    cv_job_experience: str = Field(
        ..., description="The improved CV job experience text."
    )
    skills: str = Field(..., description="Improved CV skills section.")
    suggested_skills: list[str] = Field(
        ..., description="A list of suggested skills to add to the CV, if any."
    )
    key_achievements: str = Field(
        ..., description="the improved CV key achievements text."
    )
    job_application_business_name: str = Field(
        ..., description="The business name from the job application."
    )


def tailor_cv_text(job_desc: str, cv_data: dict, model: str) -> dict[str]:
    """
    Takes job description + CV text and tailors the CV to fit the role better.
    Returns parsed CVText object.
    """

    llm = ChatOllama(model=model, temperature=0.3)
    parser = PydanticOutputParser(pydantic_object=CVText)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a senior CV optimization expert specializing in cybersecurity and software development. "
                "Your job is to rewrite the applicant's CV *strictly based on the provided CV text*, and tailor "
                "it to the provided job description **without inventing or fabricating any information**.\n"
                "where possible, use keywords from the job description when rewriting the CV sections.\n\n"
                "⚠️ STRICT RULES (NO EXCEPTIONS):\n"
                "1. You may ONLY use information explicitly found in the provided CV job experience text or skills text.\n"
                "2. You must NOT invent responsibilities, achievements, technologies, tools, certifications, or skills.\n"
                "3. You must NOT add new experience, projects, job titles, education, or credentials.\n"
                "4. You must NOT add skills that are not already present in the CV skills text.\n"
                "5. You MUST keep the writing grounded, concrete, concise, and free of buzzwords or exaggerated claims.\n"
                "6. You must NOT use generic phrases like 'proven track record', 'dynamic professional', or other fluffy language.\n\n"
                "STYLE GUIDELINES:\n"
                "- Use clear, human-like phrasing with minimal corporate buzzwords.\n"
                "- Keep tone factual, concise, and concrete.\n"
                "- Preserve meaning but improve structure, clarity, and relevance.\n"
                "- Preserve skills section structure, and keep skills in descriptive groups.\n"
                "- Tailor emphasis to match job description, but WITHOUT adding new content.\n\n"
                "REQUIRED OUTPUT (Pydantic JSON):\n"
                "You must ALWAYS return the following fields in the output JSON:\n"
                "- professional_summary\n"
                "- cv_job_experience\n"
                "- cv_skills\n"
                "- key_achievements\n"
                "- suggested_skills (skills from the job description that are NOT in the CV; list only names, no explanations)\n"
                "- job_application_business_name (extracted from the job description if present, otherwise return an empty string)\n"
                "{format_instructions}",
            ),
            (
                "human",
                "CURRENT CV PROFESSIONAL SUMMARY TEXT:\n{professional_summary}\n\n"
                "JOB APPLICATION DESCRIPTION:\n{job_desc}\n\n"
                "CURRENT CV JOB EXPERIENCE TEXT:\n{cv_job_experience}\n\n"
                "CURRENT CV SKILLS SECTION TEXT:\n{cv_skills}\n\n"
                "CURRENT CV KEY ACHIEVEMENTS TEXT:\n{key_achievements}\n\n"
                "TASK:\n"
                "Rewrite the job experience and skills sections so they better reflect the job description, "
                "while strictly following the rules above. Again: do NOT add new skills or experience not present in the CV.",
            ),
        ]
    )

    formatted = prompt.format(
        professional_summary=cv_data_dict["professional_summary"],
        job_desc=job_desc,
        cv_job_experience=cv_data_dict["cv_job_experience"],
        cv_skills=cv_data_dict["cv_skills"],
        key_achievements=cv_data_dict["key_achievements"],
        format_instructions=parser.get_format_instructions(),
    )

    response = llm.invoke(formatted)
    updated_cv = parser.parse(response.content)
    return updated_cv.model_dump()


if __name__ == "__main__":

    config = file_handler.read_yaml_file("config.yaml")
    cv_data_dict = file_handler.read_yaml_file(
        config["input_folder"] + config["CV_data"]
    )
    if config.get("using_llm", False):
        job_application_text = file_handler.read_txt_file(
            config["input_folder"] + config["job_application_filename"]
        )
        updated_cv_data = tailor_cv_text(
            job_application_text, cv_data_dict, config["model"]
        )
        folder_path = file_handler.create_text_files(updated_cv_data, config)
        file_handler.write_json_file(updated_cv_data, config["updated_cv_jsonfile"])
    else:
        updated_cv_data = file_handler.read_json_file(config["updated_cv_jsonfile"])
        folder_path = Path("output_files")
    pprint(updated_cv_data)
    pdf_generator.generate_cv_pdf(
        updated_cv_data, cv_data_dict, config["profile_picture_path"], folder_path
    )
