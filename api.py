import os
from openai import OpenAI
from dotenv import load_dotenv


# 加载 .env 文件
load_dotenv()

# 从环境变量里读取 API key
api_key = os.getenv("DEEPSEEK_API_KEY")


client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)


def chat_with_waifu(messages, waifu=None):
    """
    调用 DeepSeek API，获取回复。

    参数:
        messages:
            要发给 LLM 的完整上下文。
            格式是：
            [
                {"role": "system", "content": "..."},
                {"role": "user", "content": "..."}
            ]

        waifu:
            保留这个参数只是为了兼容 main.py 里原来的调用：
                api.chat_with_waifu(api_messages, character)

            以后也可以彻底删掉

    返回:
        LLM 返回的文本内容。
    """

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
        stream=False
    )

    return response.choices[0].message.content