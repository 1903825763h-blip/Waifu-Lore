import json
import api
class Waifu:
    def __init__(self, name, introduction):
        self.name = name
        self.introduction = introduction



def load_character():
    with open("character.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    tsuki = Waifu(
        data["name"],
        data["introduction"],
    )
    return tsuki

def main():
    tsuki = load_character()
    while True:
        message = input("我:")
        if message == "结束":
            break
        reply = api.chat_with_waifu(message,tsuki)
        print(f"{tsuki.name}:{reply}")

if __name__ == "__main__":
    main()