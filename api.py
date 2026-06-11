import os
from openai import OpenAI
from dotenv import load_dotenv

def chat_with_waifu(message,waifu):
    load_dotenv()

    api_key = os.getenv("DEEPSEEK_API_KEY")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com"
    )

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "system",
                "content": f"{waifu.introduction}"
            },
            {
                "role": "user",
                "content": f"{message}"
            }
        ],
        stream=False
    )

    return (f"{response.choices[0].message.content}")


