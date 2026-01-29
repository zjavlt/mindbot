from gemini import Gemini
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import datetime
import json
from recording import organize_user, get_user_data, initiate as initiate_recorder, close_client as close_recorder
import atexit

# discord
intent = discord.Intents.default()
intent.emojis = True
intent.message_content = True
intent.messages = True
bot = commands.Bot(command_prefix="!", intents=intent)
client = Gemini() #gemini.py에서 가져온 함수
recorder = initiate_recorder()
trigger_word = "::"

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"discord login success as {bot.user}")
    except Exception as e:
        print(f"명령어 동기화 실패: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    userLastMessage = message.content

    if userLastMessage.startswith(trigger_word):
        userLastMessage = userLastMessage[len(trigger_word):]

        if len(userLastMessage.strip()) != 0:
            try:
                async with message.channel.typing():
                    data = get_user_data(str(message.author.id))
                    name = message.author.name
                    if str(message.author.id) not in data:
                        characteristics = []
                    else:
                        characteristics = data[str(message.author.id)]["characteristics"]
                    prompt = f"{characteristics}\n======\n{userLastMessage}"
                    response = client.respond_to_chat(prompt)
                if response and hasattr(response, 'text'):
                    organize_user(str(message.author.id), str({userLastMessage: response.text})+"======"+str(characteristics), name, recorder)
                    await message.channel.send(response.text)
                else:
                    print(response)
                    await message.channel.send("ERROR: Failed to fetch response from API.")
            except Exception as e:
                print(f"Error: {e}")
                await on_message(message)
        else:
            return
    else:
        return

def exit_handler():
    print("프로그램 종료 중... Gemini 클라이언트를 닫습니다.")
    client.closeClient()
    close_recorder(recorder)
atexit.register(exit_handler)
try:
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        print("Unable to fetch discord token")
    else:
        bot.run(token)
except discord.errors.LoginFailure:
    print("Invalid Discord token provided.")
except Exception as e:
    print("Unexpected error occurred:", e)


