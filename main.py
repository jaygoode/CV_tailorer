# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from pprint import pprint
import file_handler



class CVText(BaseModel):
    job_experience: str = Field(..., description="The improved CV job experience text.")
    skills: str = Field(..., description="Improved CV skills section.")
    suggested_skills: list[str] = Field(..., description="A list of suggested skills to add to the CV, if any.")
    job_application_business_name: str = Field(..., description="The business name from the job application.")
    model: str = Field(default="llama2", description="The AI model used to generate the CV content.")


def tailor_cv_text(job_desc: str, cv_data:dict, model: str) -> dict[str]:
    """
    Takes job description + CV text and tailors the CV to fit the role better.
    Returns parsed CVText object.
    """
    
    llm = ChatOllama(model=model, temperature=0.3)
    parser = PydanticOutputParser(pydantic_object=CVText)
    prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a senior CV optimization expert specializing in cybersecurity and software development. "
     "Your job is to rewrite the applicant's CV *strictly based on the provided CV text*, and tailor "
     "it to the provided job description **without inventing or fabricating any information**.\n\n"

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
     "- Tailor emphasis to match job description, but WITHOUT adding new content.\n\n"

     "REQUIRED OUTPUT (Pydantic JSON):\n"
     "You must ALWAYS return the following fields in the output JSON:\n"
     "- job_experience\n"
     "- skills\n"
     "- suggested_skills (skills from the job description that are NOT in the CV; list only names, no explanations)\n"
     "- job_application_business_name (extracted from the job description if present, otherwise return an empty string)\n"
     "- model\n\n"
     "{format_instructions}"
    ),

    ("human",
     "JOB APPLICATION DESCRIPTION:\n{job_desc}\n\n"
     "CURRENT CV JOB EXPERIENCE TEXT:\n{cv_job_experience_text}\n\n"
     "CURRENT CV SKILLS SECTION TEXT:\n{cv_skills_text}\n\n"
     "TASK:\n"
     "Rewrite the job experience and skills sections so they better reflect the job description, "
     "while strictly following the rules above. Again: do NOT add new skills or experience not present in the CV.")
])

    formatted = prompt.format(
        job_desc=job_desc,
        cv_job_experience_text=cv_data_dict["cv_job_experience_text"],
        cv_skills_text=cv_data_dict["cv_skills_text"],
        format_instructions=parser.get_format_instructions(),
    )

    response = llm.invoke(formatted)
    updated_cv = parser.parse(response.content)
    return updated_cv.model_dump()

if __name__ == "__main__":
    config = file_handler.read_yaml_file("config.yaml")
    cv_data_dict = file_handler.read_yaml_file(config["input_folder"] + config["CV_data"])
    job_application_text = file_handler.read_txt_file(config["input_folder"] + config["job_application_filename"])
    updated_cv = tailor_cv_text(job_application_text, cv_data_dict, config["model"])
    file_handler.write_to_text_file(updated_cv, config)
    pprint(updated_cv)