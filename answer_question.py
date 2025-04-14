from openai import OpenAI
import yaml
import pprint
import datetime
import os
import chardet
import pdfplumber
from dotenv import load_dotenv
import os
from AIClient import AIClient
       
load_dotenv()


def load_from_folder_to_text(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if len(files) != 1:
        raise ValueError(f"Expected exactly one file in {folder_path}, found {len(files)}.")
    
    file_path = os.path.join(folder_path, files[0])
    
    # Open the file in binary mode to detect the encoding
    with pdfplumber.open(file_path) as pdf:
        text = ""
        
        # Extract text from each page
        for page in pdf.pages:
            text += page.extract_text()
    return text

def answer_question(
    client: AIClient,
    question: str,
    length: str = "One paragraph",
    cover_letter_path: str = r"user_writing\cover_letter",
    resume_path: str = r"user_writing\resume",
    model: str = "gpt-4o-mini",
    resume_bool: bool = True
):
    """
    # Load user experience statement
    with open(statement_path, "r") as f:
        statement = yaml.safe_load(f)["years_of_experience_statement"]
    """
    # Load resume from plain text or markdown
    # Load cover letter from plain text or markdown
    cover_letter = load_from_folder_to_text(cover_letter_path)
    resume = load_from_folder_to_text(resume_path)

    current_year = datetime.datetime.now().year

    # Scaffolding: hardcoded system and assistant messages
    client.add_messages([
        {
            "role": "system",
            "content": f"You are an expert imitator, and will copy this person's writing exactly. Your tone, knowledge, experiences, writing style, sentence length, and professionalism will match the provided writing samples perfectly. You will have no deviations in writing style, and you will not include any information that is not provided or easy to deduct. You know the current year is {current_year}"
        },
        {
            "role": "assistant",
            "content": "I will analyze the provided writing sample and resume and be ready to imitate the writing and knowledge exactly."
        },
        {
            "role": "user",
            "content": f"Cover Letter Sample: {cover_letter}"
        },
        {
            "role": "user",
            "content": f"Resume:\n{resume}"
        },
    ])
    client.add_cot_message()
    client.add_final_answer_message(formatter=f"Now, respond to the question with the same tone and style as the provided writing samples. Length: {length}.")
    result = client.generate()
    # Final answer
    return result
    
def ai_get_exp(question,length=None):
    client = AIClient()
    answer = answer_question(client,question,length)
    return answer
