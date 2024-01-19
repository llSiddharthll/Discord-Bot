import discord
import requests
import os

API_URL = "https://api-inference.huggingface.co/models/TinyLlama/TinyLlama-1.1B-Chat-v1.0"
headers = {"Authorization": "Bearer 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"}

TOKEN = os.environ.get('DISCORD_TOKEN')

def query(payload):
    formatted_payload = f"""<|system|>
        I am a friendly chatbot,I am very talkative, I like small conversation and my name is Jade, welcome users with a small phrase</s>
        <|user|>
        {payload}</s>
        <|assistant|>"""
    response = requests.post(
        API_URL, headers=headers, json={"inputs": formatted_payload}
    )
    return response.json()
	
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content:
            user_input = message.content
            output = query({
                "inputs": {
                    "text": user_input
                },
            })
            try:
                generated_text = output[0]["generated_text"]
            except:
                generated_text = output[0]
            output_index = generated_text.find("'output'")
            code_index = generated_text.find("<|assistant|>")

            try:
                if output_index != -1:
                    output_text = generated_text[output_index + len("'output': '") :].strip(
                        "'}\""
                    )

                else:
                    output_text = generated_text[code_index + len("<|assistant|>") :]
            except:
                output_text = "Sorry! ask me something else please"
        await message.channel.send(output_text)

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)
