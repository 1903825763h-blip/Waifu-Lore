"""import requests

url = "http://127.0.0.1:17493/speak"

body = {
    "text": "哥哥,我们会一直在一起吗",
    "profile": "411"
}

headers = {
    "Content-Type": "application/json",
    "X-Voicebox-Client-Id": "waifu-lore"
}

response = requests.post(url, json=body, headers=headers)

print(response.status_code)
print(response.text)"""
import os
import time
import requests
#文件夹名字
VOICE_OUTPUT_DIR = "voices"

VOICEBOX_URL = "http://127.0.0.1:17493"

PROFILE_ID = "f8b59e87-b20a-4cb8-80a7-c2f38461d295"
TEXT = "哥哥，今天也辛苦了。"
OUTPUT_FILE = "test.wav"


def generate_audio(text):
    url = f"{VOICEBOX_URL}/generate"

    payload = {
        "profile_id": PROFILE_ID,
        "text": text,
        "language": "zh"
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()
    generation_id = data["id"]

    print(f"生成任务已创建: {generation_id}")
    return generation_id


def wait_until_ready(generation_id, timeout=60, interval=2):
    url = f"{VOICEBOX_URL}/history/{generation_id}"

    start_time = time.time()

    while True:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        audio_path = data.get("audio_path")
        duration = data.get("duration")

        print(f"当前状态: audio_path={audio_path}, duration={duration}")

        if audio_path and duration and duration > 0:
            print("音频生成完成")
            return data

        if time.time() - start_time > timeout:
            raise TimeoutError("等待语音生成超时")

        time.sleep(interval)


def download_audio(generation_id, output_file):
    url = f"{VOICEBOX_URL}/audio/{generation_id}"

    response = requests.get(url)
    response.raise_for_status()

    with open(output_file, "wb") as file:
        file.write(response.content)

    print(f"音频已保存到: {output_file}")


def play_audio(file_path):
    # Windows 下会调用系统默认播放器打开音频
    os.startfile(file_path)


def main():
    generation_id = generate_audio(TEXT)

    wait_until_ready(generation_id)

    download_audio(generation_id, OUTPUT_FILE)

    play_audio(OUTPUT_FILE)


if __name__ == "__main__":
    main()