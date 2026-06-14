import os
import json

#路径文件夹名字
CHARACTER_DIR = "characters"
#导入类
class Waifu:
    def __init__(self, name, prompt, character_id):
        self.name = name
        self.prompt = prompt
        self.character_id = character_id

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

"""if __name__ == "__main__":
    character = choose_character()

    if character:
        print("你选择了:", character["name"])
        print(character["prompt"])
"""