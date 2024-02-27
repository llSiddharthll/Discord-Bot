import requests

def GeminiChat(prompt):
    # Replace "YOUR_API_KEY" with your actual API key
    API_KEY = "AIzaSyB38xndnMqkV6P8f2u7l9bcFBxjpWksjkA"

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
