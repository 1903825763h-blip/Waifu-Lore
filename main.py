import api
import voice_generate
import re
import character_manager


# 删除括号和括号内的内容
def clean_text_for_voice(text):
    # 删除中文括号里的内容：（...）
    text = re.sub(r"（.*?）", "", text)

    # 删除英文括号里的内容：(...)
    text = re.sub(r"\(.*?\)", "", text)

    # 去掉前后空格
    text = text.strip()

    return text


def main():
    # 选择角色
    # choose_character() 会返回一个 Waifu 对象
    # 如果没有成功选择角色，就继续让用户选择
    character = None

    while not character:
        character = character_manager.choose_character()

        if not character:
            continue

    # 是否打开语音
    # strip() 去掉前后空格
    # lower() 把 YES / Yes / yes 都变成 yes
    voice_or_not = input("是否打开语音功能，会增加额外的延迟: (yes/no) ")
    voice_or_not = voice_or_not.strip().lower()

    # 读取角色 prompt
    # system 用于告诉 AI 当前角色设定
    messages = [
        {
            "role": "system",
            "content": character.prompt
        }
    ]

    print("tips: 安全词为 end，输入 end 则结束对话")

    while True:
        # 接收用户输入
        message = input("我:")

        #end则结束
        if message == "end":
            break

        # 保存用户当前输入
        messages.append({
            "role": "user",
            "content": message
        })

        # 发送给 API 的上下文
        # messages[0] 是 system prompt
        # messages[-n:] 是最近 n条对话，避免上下文太长
        api_messages = [messages[0]] + messages[-100:]

        # 调用 API 获取角色回复
        reply = api.chat_with_waifu(api_messages, character)

        # 保存 AI 回复
        messages.append({
            "role": "assistant",
            "content": reply
        })

        # 清理语音文本，避免把括号动作读出来0
        replytext = clean_text_for_voice(reply)

        # 如果开启语音功能
        if voice_or_not == "yes":
            print("请耐心等待语音生成")

            try:
                # 先生成语音文件，但不播放
                audio_file = voice_generate.generate_voice_file(replytext)

                # 语音准备好以后，再显示文字
                print(f"{character.name}:{reply}", flush=True)

                # 播放语音
                if audio_file:
                    voice_generate.play_audio(audio_file)

            except Exception as e:
                # 如果语音失败，文字仍然正常显示
                print(f"{character.name}:{reply}", flush=True)
                print(f"[语音生成失败，请确定已启动 voicebox 服务]: {e}")

        # 如果不开语音，直接显示文字
        else:
            print(f"{character.name}:{reply}", flush=True)


if __name__ == "__main__":
    main()