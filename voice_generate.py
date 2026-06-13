import time
import os
import requests
from playsound import playsound


# 语音保存文件夹
VOICE_OUTPUT_DIR = "voices"

# Voicebox 本地服务地址
VOICEBOX_URL = "http://127.0.0.1:17493"

# Voicebox voice profile id
PROFILE_ID = "f8b59e87-b20a-4cb8-80a7-c2f38461d295"


def generate_audio(text):
    """
    向 Voicebox 发送生成语音请求。

    参数:
        text: 要转换成语音的文本

    返回:
        generation_id: Voicebox 返回的生成任务 id

    对应接口:
        POST /generate
    """

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

    return generation_id


def wait_until_ready(generation_id, timeout=60, interval=2):
    """
    等待 Voicebox 生成语音完成。

    参数:
        generation_id: generate_audio() 返回的生成任务 id
        timeout: 最多等待多少秒
        interval: 每隔多少秒查询一次状态

    返回:
        data: Voicebox 生成完成后的历史记录数据

    逻辑:
        不断请求 /history/{generation_id}
        如果 audio_path 存在，并且 duration > 0，说明音频已经生成完成。
    """

    url = f"{VOICEBOX_URL}/history/{generation_id}"
    start_time = time.time()

    while True:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        audio_path = data.get("audio_path")
        duration = data.get("duration")
        error = data.get("error")

        if error:
            raise RuntimeError(f"Voicebox generation failed: {error}")

        if audio_path and duration and duration > 0:
            return data

        if time.time() - start_time > timeout:
            raise TimeoutError("Voicebox generation timeout")

        time.sleep(interval)


def download_audio(generation_id):
    """
    根据 generation_id 下载生成好的音频文件。

    每次使用不同的文件名，并保存到 voices/ 文件夹中。
    例如:
        voices/voice_da26609d-e164-4915-a71c-97ff43aa9612.wav

    参数:
        generation_id: Voicebox 生成任务 id

    返回:
        output_file: 下载后的本地音频路径
    """

    url = f"{VOICEBOX_URL}/audio/{generation_id}"

    response = requests.get(url)
    response.raise_for_status()

    os.makedirs(VOICE_OUTPUT_DIR, exist_ok=True)

    output_file = os.path.join(
        VOICE_OUTPUT_DIR,
        f"voice_{generation_id}.wav"
    )

    with open(output_file, "wb") as file:
        file.write(response.content)

    return output_file


def generate_voice_file(text):
    """
    生成语音文件，但不播放。

    这个函数用于 main.py 控制显示时机。

    流程:
        1. 发送生成请求
        2. 等待生成完成
        3. 下载音频
        4. 返回音频文件路径

    参数:
        text: 要转换成语音的文本

    返回:
        audio_file: 本地音频文件路径
        如果 text 为空，返回 None
    """

    if not text:
        return None

    generation_id = generate_audio(text)

    wait_until_ready(generation_id)

    audio_file = download_audio(generation_id)

    return audio_file


def play_audio(file_path):
    """
    在 Python 内部播放音频。

    注意:
        playsound 会阻塞程序。
        也就是音频播放完之前，程序会停在这里。
    """

    if not file_path:
        return

    playsound(file_path)


def speak(text):
    """
    简化版语音播放函数。

    其他地方如果不关心显示时机，可以直接调用:
        voice_generate.speak("要说的话")

    它会自动:
        1. 生成语音
        2. 下载音频
        3. 播放音频
    """

    audio_file = generate_voice_file(text)

    if audio_file:
        play_audio(audio_file)