import discord
import requests
import os
import io
import click
from requests import get
from uuid import uuid4
from re import findall
from curl_cffi.requests import get, RequestsError

class youChat:
    def create(self, prompt):
        resp = get(
            "https://you.com/api/streamingSearch",
            headers={
                "cache-control": "no-cache",
                "referer": "https://you.com/search?q=gpt4&tbm=youchat",
                "cookie": f"safesearch_guest=Off; uuid_guest={str(uuid4())}",
            },
            params={
                "q": prompt,
                "page": 1,
                "count": 10,
                "safeSearch": "Off",
                "onShoppingPage": False,
                "mkt": "",
                "responseFilter": "WebPages,Translations,TimeZone,Computation,RelatedSearches",
                "domain": "youchat",
                "queryTraceId": str(uuid4()),
                "chat": [],
            },
            impersonate="chrome107",
        )
        if "youChatToken" not in resp.text:
            raise RequestsError("Unable to fetch the response.")
        return (
            "".join(
                findall(
                    r"{\"youChatToken\": \"(.*?)\"}",
                    resp.content.decode("unicode-escape"),
                )
            )
            .replace("\\n", "\n")
            .replace("\\\\", "\\")
            .replace('\\"', '"')
        )

    @staticmethod
    def chat_cli(prompt):
        """Generate completion based on the provided prompt"""
        you_chat = youChat()
        completion = you_chat.create(prompt)
        print(completion)
        
@click.option('--prompt', prompt='Enter your prompt', help='The prompt to generate a completion from.')
def youchat(prompt):
    youChat.chat_cli(prompt)

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
                    output = youchat(user_input)
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


