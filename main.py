import api
import voice_generate
import re
import character_manager
import database
import memory_manager


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
    # 初始化数据库
    database.init_db()

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

        # end则结束
        if message == "end":
            """
            主动退出时保存当前剩余聊天记录

            为什么这里也要保存：
                正常情况下，聊天记录达到 50 条才会触发压缩保存。
                但是如果用户在没有达到 50 条之前主动输入 end 退出，
                这部分聊天记录就不会被保存成长期记忆。

            所以这里的逻辑是：
                1. 取出除了 system prompt 以外的聊天记录
                2. 如果确实有聊天内容，就调用 summarize_messages() 总结
                3. 如果总结结果不是 None，就保存进数据库
                4. 最后退出程序

            注意：
                这里保存的是“当前剩余聊天记录的总结”，不是逐条保存原始聊天。
            """

            chat_messages = messages[1:]

            if chat_messages:
                summary = memory_manager.summarize_messages(chat_messages)

                if summary:
                    database.save_memory(character.character_id, summary)
                    print("[memory] 退出前的对话已保存")

            break

        # 保存用户当前输入
        messages.append({
            "role": "user",
            "content": message
        })

        # 发送给 API 的上下文
        # messages[0] 是 system prompt
        # messages[1:] 是除了 system prompt 以外的聊天记录
        # messages[1:][-100:] 是最近 100 条聊天，避免上下文太长
        api_messages = [messages[0]] + messages[1:][-100:]

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

        """
        聊天记录压缩保存逻辑

        为什么放在回复显示之后：
            如果先压缩，再显示回复，
            那么刚好达到 50 条时，用户会感觉程序卡住，
            因为它要先等待 LLM 总结旧聊天记录。
            所以这里先显示/播放当前回复，再做记忆压缩。

        设计逻辑：
            messages[0] 是 system prompt，不参与总结。
            messages[1:] 才是真正的 user / assistant 聊天记录。

            当聊天记录达到 50 条：
                old_messages = 较旧的 40 条
                recent_messages = 最近的 10 条

            old_messages 会被总结成长期记忆，保存进 SQLite。
            recent_messages 会被保留下来，保证当前对话不会突然断掉。
        """

        # 获取除了 system prompt 以外的聊天记录
        # messages[0] 是 system prompt，不应该参与总结
        chat_messages = messages[1:]

        # 如果聊天记录达到 n 条，就进行压缩
        if len(chat_messages) >= 50:
            # old_messages 是较旧的 n 条，用来总结成长期记忆
            old_messages = chat_messages[:-10]

            # recent_messages 是最近的 -n 条，用来保持当前对话连贯
            recent_messages = chat_messages[-10:]

            # 调用 LLM 总结较旧的聊天记录
            summary = memory_manager.summarize_messages(old_messages)

            # 如果总结结果不是 None，就保存进数据库
            if summary:
                database.save_memory(character.character_id, summary)

            # 重新整理 messages
            # 保留 system prompt + 最近 10 条聊天
            messages = [messages[0]] + recent_messages
            print("[memory] 对话已压缩并保存")


if __name__ == "__main__":
    main()