from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
import json


def initiate():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY2"))
    return client

def get_user_data(user_id):
    try:
        with open("userdata.json", "r", encoding="utf-8") as f:
            userdata = json.load(f)
        return userdata
    except FileNotFoundError:
        return {}
    
def organize_user(user_id, conversation: str, username: str, client=None):
    userdata = get_user_data(user_id)
    if user_id in userdata:
        pass
    else:
        userdata[user_id] = {"username": username, "characteristics": []}
    instruction = open('instruction_organizer.txt', 'r', encoding='utf-8').read()
    prompt = conversation + "\n======\n" + str(userdata[user_id]["characteristics"])
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=genai.types.GenerateContentConfig(
                system_instruction=instruction
            )
        )
    except Exception:
        organize_user(user_id, conversation, username, client)
        return
    userdata[user_id]["characteristics"] = eval(response.text)
    with open("userdata.json", "w", encoding="utf-8") as f:
        json.dump(userdata, f, ensure_ascii=False, indent=4)

def close_client(client):
    client.close()