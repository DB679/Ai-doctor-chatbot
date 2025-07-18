import os
import base64
from groq import Groq

# Optional dotenv load
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def encode_image(image_path):   
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_with_groq(query, encoded_image=None):
    client = Groq(api_key=GROQ_API_KEY)

    # Choose model based on presence of image
    if encoded_image:
        model = "meta-llama/llama-4-scout-17b-16e-instruct"  # Vision + text
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
                    }
                ],
            }
        ]
    else:
        model = "llama3-70b-8192"  # Text-only
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model=model
    )

    return chat_completion.choices[0].message.content
