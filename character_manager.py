import os
import json

#路径文件夹名字
CHARACTER_DIR = "characters"
#导入类
class Waifu:
    def __init__(self, name, prompt, character_id):
        self.name = name
        self.prompt = prompt
        self.character_id = character_id#文件夹的名字为id

def list_characters():
    #如果不存在文件夹则创建并且返回空列表
    if not os.path.exists(CHARACTER_DIR):
        os.makedirs(CHARACTER_DIR)
        return []
    #角色列表存储
    characters = []

    for item in os.listdir(CHARACTER_DIR):
        path = os.path.join(CHARACTER_DIR,item)

        if os.path.isdir(path):
            characters.append(item)

    return characters
#接收角色id
def load_character(character_folder):
    character_path = os.path.join(CHARACTER_DIR, character_folder)

    json_path = os.path.join(character_path, "character.json")
    prompt_path = os.path.join(character_path, "prompt.md")

    with open(json_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt = file.read()

    character = Waifu(
        name=data["name"],
        prompt=prompt,
        character_id=character_folder
    )

    return character


#显示列表,返回角色数据
def choose_character():
    characters = list_characters()

    if not characters:
        print("还没角色呢")
        return None
    print("\n请选择角色")
    #把角色编号对应上角色,从1开始
    for index, character_folder in enumerate(characters, start=1):
        character = load_character(character_folder)
        print(f"{index}. {character.name} ({character_folder})")
    #接收输入
    choice = input("输入编号: ")
    #判断是否数字,并转换成int类型
    if not choice.isdigit():
        print("请输入数字。")
        return None
    choice = int(choice)

    if choice < 1 or choice > len(characters):
        print("编号不存在")
        return None

    selected_id = characters[choice - 1]
    selected_character = load_character(selected_id)
    return selected_character

def create_character():
    # 接收角色文件夹名
    character_id = input("请输入角色文件夹名:")
    character_id = character_id.strip()

    # 判断角色文件夹名是否为空
    if not character_id:
        print("角色文件夹名不能为空")
        return None

    # 拼接角色文件夹路径
    character_path = os.path.join(CHARACTER_DIR, character_id)

    # 如果角色已经存在，就不重复创建
    if os.path.exists(character_path):
        print("这个角色已经存在")
        return None

    # 接收角色显示名称
    character_name = input("请输入角色名字: ")
    character_name = character_name.strip()

    # 判断角色名字是否为空
    if not character_name:
        print("角色名字不能为空")
        return None

    # 创建角色文件夹
    os.makedirs(character_path)

    # 拼接 character.json 路径
    json_path = os.path.join(character_path, "character.json")

    # 要写入 json 的角色数据
    character_data = {
        "name": character_name
    }

    # 写入 character.json
    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(character_data, file, ensure_ascii=False, indent=4)

    print(f"角色创建成功: {character_name} ({character_id})")

    # 接收角色 prompt
    print("请输入角色 prompt，输入完成后直接回车即可：")
    character_prompt = input("prompt: ")
    character_prompt = character_prompt.strip()

    # 判断 prompt 是否为空
    if not character_prompt:
        print("prompt 不能为空")
        return None

    # 拼接 prompt.md 路径
    prompt_path = os.path.join(character_path, "prompt.md")

    # 写入 prompt.md
    with open(prompt_path, "w", encoding="utf-8") as file:
        file.write(character_prompt)

    return character_id

if __name__ == "__main__":

    print()