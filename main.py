import json
import api
import voice_generate
import re



class Waifu:
    def __init__(self, name, introduction):
        self.name = name
        self.introduction = introduction


#从json里读取角色名字,prompt.md读取角色介绍
def load_character():
    with open("character.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    with open("prompt.md", "r", encoding="utf-8") as prom:
        prompt = prom.read()
    character = Waifu(
        data["name"],
        prompt,
    )
    return character
#删除括号和内的内容
def clean_text_for_voice(text):
    # 删除中文括号里的内容：（...）
    text = re.sub(r"（.*?）", "", text)

    # 删除英文括号里的内容：(...)
    text = re.sub(r"\(.*?\)", "", text)

    # 去掉前后空格
    text = text.strip()

    return text

def main():
    character = load_character()
    #读取提示词
    messages =[
        {
            "role": "system",
            "content": character.introduction
        }
    ]
    while True:
        message = input("我:")
    #输入结束时结束对话
        if "结束" in message:
            break
    #输入当前信息并且保存
        messages.append({
            "role": "user",
            "content": message
        })



        api_messages = [messages[0]] + messages[-10:]

        reply = api.chat_with_waifu(api_messages,character)
        messages.append({
            "role": "assistant",
            "content": reply
        })
        replytext = clean_text_for_voice(reply)
        print("请耐心等待语音生成")
        try:
            audio_file = voice_generate.generate_voice_file(replytext)

            print(f"{character.name}:{reply}", flush=True)

            if audio_file:
                voice_generate.play_audio(audio_file)

        except Exception as e:
            print(f"{character.name}:{reply}", flush=True)
            print(f"[语音生成失败，已跳过]: {e}")



if __name__ == "__main__":
    main()