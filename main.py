from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class CVText(BaseModel):
    job_experience: str = Field(..., description="The improved CV job experience text.")
    skills: str = Field(..., description="Improved skills section.")
    model: str = Field(default="llama2", description="The AI model used to generate the CV content.")


def tailor_cv_text(job_desc: str, cv_text: dict) -> CVText:
    """
    Takes job description + CV text and tailors the CV to fit the role better.
    Returns parsed CVText object.
    """

    # ---- Model ----
    llm = ChatOllama(model="qwen3:30b", temperature=0.3)

    # ---- Output parser ----
    parser = PydanticOutputParser(pydantic_object=CVText)

    # ---- Prompt ----
    prompt = ChatPromptTemplate.from_messages([
        ("system",
         "You are a senior CV optimization expert specializing in cybersecurity and software development. "
         "Rewrite and tailor the candidate’s CV to match the job description. "
         "Output MUST follow the Pydantic format.\n\n"
         "{format_instructions}"
         ),
        ("human",
         "JOB DESCRIPTION:\n{job_desc}\n\n"
         "CURRENT CV SECTIONS:\n{cv_text}\n\n"
         "Please rewrite them to better match the job.")
    ])

    # ---- Format prompt ----
    formatted = prompt.format(
        job_desc=job_desc,
        cv_text=cv_text,
        format_instructions=parser.get_format_instructions(),
    )

    # ---- AI call ----
    response = llm.invoke(formatted)

    # ---- Parse structured output ----
    return parser.parse(response.content)


# -----------------------------------------------------------

if __name__ == "__main__":
    job_desc = "Penetration tester role requiring Python, network security, OSINT, Linux, and web exploitation."
    cv_text = {
        "job_experience": "3 years Python RPA developer; automation work; some cybersecurity courses.",
        "skills": "Python, Linux, HTML, JS, some pentesting labs."
    }

    updated = tailor_cv_text(job_desc, cv_text)
    print(updated)
