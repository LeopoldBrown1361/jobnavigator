from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Get the single file from resume folder
class AIClient:
    def __init__(self, api_key = os.getenv("OPENAI_API_KEY"), messages=[]):
        self.client = OpenAI()
        self.messages = messages

    def add_messages(self,new_messages: dict|list[dict]):
        if type(new_messages) ==list:
            for msg in new_messages:
                self.messages.append(msg)
        elif type(new_messages) == dict:
            self.messages.append(new_messages)

    def get_messages(self):
        return self.messages
    
    def add_cot_message(self):
        self.messages.append(
            {
                "role": "system",
                "content": "reason step-by-step about the question given the context. Explore answers and use this as a scratch pad to enumerate your thinking, but don't come to a conclusive answer yet."
            })
    
    def generate(self):
        model_answer = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,
        )
        self.messages.append({"role": "assistant", "content": model_answer.choices[0].message.content})
        return model_answer.choices[0].message.content
    
    def add_final_answer_message(self, formatter: str = "now, give a singular number answer to the question"):
        self.messages.append({"role": "user", "content": formatter})
       