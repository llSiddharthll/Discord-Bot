import requests
from bs4 import BeautifulSoup

def fetch_ai_content_with_bs4(url, prompt):
    # Set up the payload data
    payload = {
        "chat-input": prompt,
        # Add any other required parameters here
    }

    # Make a POST request to the URL
    response = requests.post(url, data=payload)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the element containing the AI-generated content
    result_element = soup.find("div", class_="wpaicg-ai-message")

    # Get the text content of the element
    result = result_element.text.strip() if result_element else "Result not found"

    return result

# Example usage:
url = "https://chatgptt.me/"
prompt = "hello"

result = fetch_ai_content_with_bs4(url, prompt)
print(result)
