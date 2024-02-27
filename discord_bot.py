import discord
import requests
import os
import io

def GeminiChat(prompt):
    # Replace "YOUR_API_KEY" with your actual API key
    API_KEY = os.environ.get("Gemini_Key")

    # Define the request data
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}],
            }
        ]
    }

    # Set the request headers
    headers = {"Content-Type": "application/json"}

    # Construct the API endpoint URL with the API key
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"

    # Send the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check for successful response
    if response.status_code == 200:
    # Parse the JSON response
        response_data = response.json()
        generated_text = response_data["candidates"][0]['content']['parts'][0]['text']
    # Access the generated text from the response
        return generated_text
    
    else:
        return {"Error" : response.status_code}

IMAGE_API_URL = "https://api-inference.huggingface.co/models/segmind/Segmind-Vega"
headers = {"Authorization": "Bearer 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"}
TOKEN = os.environ.get("DISCORD_TOKEN")


def query_image(payload):
    response = requests.post(IMAGE_API_URL, headers=headers, json=payload)
    return response.content


class MyClient(discord.Client):
    async def on_ready(self):
        print("Logged on as", self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content:
            user_input = message.content.lower()

            if user_input.startswith(("itachi", "/bro", "bro", "jade", "bot")):
                async with message.channel.typing():
                    words = user_input.split()
                    new_sentence = " ".join(words[1:])
                    output = GeminiChat(new_sentence)
                    await message.channel.send(output)

            elif user_input.startswith(("generate", "make")):
                async with message.channel.typing():
                    image_bytes = query_image({"inputs": user_input})
                    image = io.BytesIO(image_bytes)
                    image.seek(0)
                    try:
                        await message.channel.send(
                            f"{message.author.mention}, here's your generated image:",
                            file=discord.File(image, "image.jpg"),
                        )
                    except:
                        await message.channel.send(
                            "Sorry I cannot generate it, try something else please!"
                        )


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN)
