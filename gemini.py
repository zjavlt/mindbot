from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
from recording import organize_user, get_user_data

class Gemini(object):
    regular_instruction = open('instruction.txt', 'r', encoding='utf-8').read()
    def __init__(self):
        self.client = self.initiate()
        self.load_instruction()
        
    def initiate(self):
        client = genai.Client(api_key=str(os.getenv("GOOGLE_API_KEY")))
        return client
    
    def load_instruction(self):
        load_dotenv()
        self.instruction = Gemini.regular_instruction

    def respond_to_chat(self, prompt: str):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=self.instruction)
        )
        return response

    def closeClient(self):
        self.client.close()