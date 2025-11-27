# from langchain_community.chat_models import ChatOllama
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import yaml 
from pprint import pprint


class CVText(BaseModel):
    job_experience: str = Field(..., description="The improved CV job experience text.")
    skills: str = Field(..., description="Improved skills section.")
    model: str = Field(default="llama2", description="The AI model used to generate the CV content.")

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

def tailor_cv_text(job_desc: str, cv_job_experience_text: str, cv_skills_text:str) -> CVText:
    """
    Takes job description + CV text and tailors the CV to fit the role better.
    Returns parsed CVText object.
    """

    llm = ChatOllama(model="qwen3:30b", temperature=0.3)
    parser = PydanticOutputParser(pydantic_object=CVText)
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a senior CV optimization expert specializing in cybersecurity and software development. "
         "Rewrite and tailor the candidate's CV to match the job description. "
         "Output MUST follow the Pydantic format.\n\n"
         "{format_instructions}"
         ),
        ("human",
         "JOB APPLICATION DESCRIPTION:\n{job_desc}\n\n"
         "CURRENT CV JOB EXPERIENCE TEXT:\n{cv_job_experience_text}\n\n"
         "CURRENT CV SKILLS SECTION TEXT:\n{cv_skills_text}\n\n"
         "Please rewrite them to better match the job."
         "Do not add skills or information about the CV owner that does not already exist in the CV job experience text or skills text.")
    ])

    formatted = prompt.format(
        job_desc=job_desc,
        cv_job_experience_text=cv_job_experience_text,
        cv_skills_text=cv_skills_text,
        format_instructions=parser.get_format_instructions(),
    )

    response = llm.invoke(formatted)
    updated_cv = parser.parse(response.content)
    return updated_cv.model_dump()


# -----------------------------------------------------------

if __name__ == "__main__":
    cv_data_filepath = "./CV_data.yaml"
    cv_data_dict = read_yaml_file(cv_data_filepath)
    updated_cv = tailor_cv_text(cv_data_dict["job_application_description"], cv_data_dict["cv_job_experience_text"], cv_data_dict["cv_skills_text"])


    pprint(updated_cv)