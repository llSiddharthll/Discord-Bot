import discord
import requests
import os
import io


API_URL = "https://api-inference.huggingface.co/models/google/gemma-2b-it"
headers = {"Authorization": "Bearer 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"}

def query(payload):
    formatted_payload = f'''
    <start_of_turn>user \n
    {payload}<end_of_turn>
    <start_of_turn>model \n
    '''
    response = requests.post(API_URL, headers=headers, json=formatted_payload)
    return response.json()
	

API_URL = "https://api-inference.huggingface.co/models/openchat/openchat-3.5-0106"
IMAGE_API_URL = "https://api-inference.huggingface.co/models/segmind/Segmind-Vega"
headers = {"Authorization": "Bearer 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"}
TOKEN = os.environ.get('DISCORD_TOKEN')

	
def query_image(payload):
    response = requests.post(IMAGE_API_URL, headers=headers, json=payload)
    return response.content

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content:
            user_input = message.content.lower()

            if user_input.startswith(("itachi", "/bro", "bro", "jade", "bot")):
                async with message.channel.typing():
                    output = query(user_input)
                    await message.channel.send(output)

            elif user_input.startswith(("generate", "make")):
                async with message.channel.typing():
                    image_bytes = query_image({"inputs": user_input})
                    image = io.BytesIO(image_bytes)
                    image.seek(0)
                    try:
                        await message.channel.send(f"{message.author.mention}, here's your generated image:", file=discord.File(image, 'image.jpg'))
                    except:
                        await message.channel.send("Sorry I cannot generate it, try something else please!")

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)


