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

请你阅读下面的用户发言，并总结出值得长期保存的信息。

重要规则：
1. 只总结 user 明确说过的信息
2. 不要根据角色设定、角色身份、恋爱关系进行补充
3. 不要记录 assistant 的人设、语气、情绪或角色扮演内容
4. 不要记录普通寒暄，例如“你好”“晚安”“在吗”
5. 只保留对未来对话有帮助的信息
6. 用简短中文总结
7. 如果没有值得保存的信息，返回：NONE
8. 每条记忆必须是完整句子
9. 每条记忆必须包含明确主语
10. 不要输出短语，例如“不喜欢吃青菜”
11. 正确格式示例：用户不喜欢吃青菜。

以下信息必须保存：
- 用户喜欢什么
- 用户不喜欢什么
- 用户讨厌什么
- 用户害怕什么
- 用户正在做什么项目
- 用户的长期目标
- 用户的重要习惯
- 用户的重要关系或现实状态
- 用户明确表达的偏好、计划、限制

输出格式：
如果有值得保存的信息，只输出记忆内容，不要解释。
如果有多条记忆，每条单独一行。
如果没有值得保存的信息，只输出 NONE。

用户发言如下：

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


"""if __name__ == "__main__":
    database.init_db()

    test_messages = [
        {"role": "user", "content": "我最近在好好学习。"},
        {"role": "assistant", "content": "哥哥终于认真学习了。"},
        {"role": "user", "content": "我已经成功了。"}
    ]

    summary = summarize_messages(test_messages)

    print("总结结果:")
    print(summary)

    if summary:
        database.save_memory("411", summary)
        print("总结已保存到数据库")"""