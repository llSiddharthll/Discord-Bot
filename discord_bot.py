import discord
import requests
import os
import io 

API_URL = "https://api-inference.huggingface.co/models/openchat/openchat-3.5-0106"
headers = {"Authorization": "Bearer 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"}
IMAGE_API_URL = (
    "https://api-inference.huggingface.co/models/dataautogpt3/ProteusV0.1"
)
TOKEN = os.environ.get('DISCORD_TOKEN')

def query(payload):
    formatted_payload = f"""
        GPT4 Correct User: Hello<|end_of_turn|>
        GPT4 Correct Assistant: Hi<|end_of_turn|>
        GPT4 Correct User: What is your name?<|end_of_turn|>
        GPT4 Correct Assistant: My name is "Itachi Uchiha" of the village "leaf", I am a conversational bot made by Siddharth<|end_of_turn|>
        GPT4 Correct User: {payload}<|end_of_turn|>
        GPT4 Correct Assistant: 
        """
    response = requests.post(
        API_URL, headers=headers, json={"inputs": formatted_payload}
    )
    return response.json()
	
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
            user_input = message.content
            if user_input.lower().startswith(("itachi", "/bro", "bro","jade","bot")):
                async with message.channel.typing():
                    output = query({
                        "inputs": {
                            "text": user_input
                        },
                    })
                    user_input = ' '.join(user_input.split()[1:])
                    output = query(user_input)
                    generated_text = output[0]["generated_text"]
                    output_index = generated_text.find(user_input)
                    output_text = generated_text[output_index + len(user_input):]
                    lines = output_text.split('\n')
                    result_output = '\n'.join(lines[2:])
                    await message.channel.send(result_output)
            
            if user_input.lower().startswith(("generate", "make")):
                async with message.channel.typing():
                    image_bytes = query_image({"inputs": user_input})  
                    image = io.BytesIO(image_bytes)
                    image.seek(0)
                    try:
                        await message.channel.send(f"{message.author.mention}, here's your generated image:",file=discord.File(image, 'image.jpg'))
                    except Exception as e:
                        print(f"Error sending image: {e}")

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)
