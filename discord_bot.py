import discord
import requests
import os
import io 

API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
headers = {"Authorization": "Bearer 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"}
IMAGE_API_URL = (
    "https://api-inference.huggingface.co/models/cagliostrolab/animagine-xl-3.0"
)
TOKEN = os.environ.get('DISCORD_TOKEN')

def query(payload):
    formatted_payload = f"""<|system|>
        Hey there! I'm Itachi Uchiha, your friendly chat companion. I love chatting about anything and everything. Whether it's tech talk, life updates, or even a joke or two, I'm here for you. Feel free to start a conversation, and let's make this chat a great experience for you!</s>
        <|user|>
        {payload}</s>
        <|assistant|>"""
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
                    try:
                        generated_text = output[0]["generated_text"]
                    except:
                        generated_text = output
                    try:
                        output_index = generated_text.find("'outputs'")
                    except:
                        try:
                            output_index = generated_text.find("<|assistant|>")
                        except:
                            output_index = generated_text

                    try:
                        if output_index != -1:
                            output_text = generated_text[output_index + len("'outputs': 'text': '") :].strip(
                                "'}\""
                            )

                        else:
                            output_text = generated_text[output_index + len("<|assistant|>") :]
                    except:
                        output_text = generated_text
                    await message.channel.send(output_text)
            
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
