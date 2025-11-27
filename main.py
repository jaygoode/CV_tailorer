from langchain_community.chat_models import ChatOllama
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class CVText(BaseModel):
    job_experience:str = Field(..., description="the CV job experience text.")
    Skills:str = Field(..., description="listed skills on the CV.")
    model: str = Field(default="llama2", description="The AI model used to generate the card content.")

def tailor_cv_text(job_desc:str, cv_text:dict) -> None:
    '''main function that takes CV text and updates it to better fit chosen job descriptions.'''
    prompt: str
    model: str = "llama2"
    system_prompt: str = "You are a senior-level professional related to the question.",
    temperature: float = 0.3
    k: int = 3

    llm = ChatOllama(model=model)

    # ---- prompt setup ----
    system_msg = SystemMessagePromptTemplate.from_template(template=system_prompt)
    human_msg = HumanMessagePromptTemplate.from_template(template=prompt)
    chat_prompt = ChatPromptTemplate.from_messages([system_msg, human_msg])

    parser = PydanticOutputParser(pydantic_object=CVText)
    formatted_prompt = chat_prompt.format_prompt(
        topic=prompt,
        format_instructions=parser.get_format_instructions(),
    )

    # ---- AI call ----
    response = llm(formatted_prompt.to_messages())
    raw_output = response.content.strip()

 

if __name__ == "__main__":
    job_desc = ""
    cv_text = ""
    tailor_cv_text(job_desc, cv_text)
