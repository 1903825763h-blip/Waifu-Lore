import api


def summarize_messages(messages):
    """
    总结一批聊天记录。
    参数:
        messages:
            一批聊天记录。
            格式和 main.py 里的 messages 一样，例如：
            [
                {"role": "user", "content": "我今天很累"},
                {"role": "assistant", "content": "哥哥辛苦了"}
            ]

    返回:
        summary:
            LLM 总结出来的一段长期记忆文本。
    """

    # 如果没有聊天记录，就没有必要总结
    if not messages:
        return None

    # 把 messages 列表转换成普通文本, LLM 更容易阅读这种格式
    conversation_text = ""

    for message in messages:
        role = message["role"]
        content = message["content"]

        conversation_text += f"{role}: {content}\n"

    # 专门用于总结记忆的 prompt
    summary_prompt = f"""
你是一个长期记忆总结器。

请你阅读下面的聊天记录，并总结出值得长期保存的信息。

要求：
1. 只保留对未来对话有帮助的信息
2. 不要逐句复述聊天记录
3. 不要保存无意义寒暄
4. 用简短中文总结
5. 如果没有值得保存的信息，返回：NONE

聊天记录如下：

{conversation_text}
"""

    # 构造发给 LLM 的 messages
    # 这里单独创建 summary_messages，避免和 main.py 的聊天 messages 混在一起
    summary_messages = [
        {
            "role": "system",
            "content": "你负责把聊天记录压缩成长期记忆。"
        },
        {
            "role": "user",
            "content": summary_prompt
        }
    ]

    # 调用 api.py 里的聊天函数
    # character传None，因为总结任务不需要角色人格
    summary = api.chat_with_waifu(summary_messages, None)

    # 去掉前后空格
    summary = summary.strip()

    # 如果 LLM 判断没有值得保存的信息，就返回 None
    if summary == "NONE":
        return None

    return summary

import database


if __name__ == "__main__":
    database.init_db()

    test_messages = [
        {"role": "user", "content": "我最近在做 Waifu Lore 项目。"},
        {"role": "assistant", "content": "哥哥终于认真做项目了。"},
        {"role": "user", "content": "我已经完成了角色选择系统和 SQLite 保存记忆。"}
    ]

    summary = summarize_messages(test_messages)

    print("总结结果:")
    print(summary)

    if summary:
        database.save_memory("411", summary)
        print("总结已保存到数据库")