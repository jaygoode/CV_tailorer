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
    job_application_business_name: str = Field(..., description="The business name from the job application.")
    model: str = Field(default="llama2", description="The AI model used to generate the CV content.")


def tailor_cv_text(job_desc: str, cv_job_experience_text: str, cv_skills_text:str) -> dict[str]:
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
         "Do not add skills or information about the CV owner that does not already exist in the CV job experience text or CV skills text.")
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

if __name__ == "__main__":
    input_fp = "./input_files"
    cv_data_dict = file_handler.read_yaml_file(f"{input_fp}/CV_data.yaml")
    job_application_text = file_handler.read_txt_file(f"{input_fp}/job_application_text.txt")
    updated_cv = tailor_cv_text(job_application_text, cv_data_dict["cv_job_experience_text"], cv_data_dict["cv_skills_text"])
    file_handler.write_to_text_file(updated_cv)
    pprint(updated_cv)