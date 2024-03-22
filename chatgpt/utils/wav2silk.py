import pilk
import sys
import subprocess

# 导入pydub库
from pydub import AudioSegment
from pydub.silence import split_on_silence
import random

def add_silence(audio_path):
    # 定义音频文件的路径
    # audio_path = "your_audio_file.wav"

    # 定义沉默的长度和阈值（单位为毫秒）
    min_silence_len = 50 # 300ms
    silence_thresh = -50 # -50dBFS

    # 定义无声时间的范围（单位为毫秒）
    min_silent_time = 200 # 300ms
    max_silent_time = 600 # 1000ms

    # 加载音频文件
    audio = AudioSegment.from_wav(audio_path)

    # 按照沉默来切分音频
    chunks = split_on_silence(audio, min_silence_len, silence_thresh)

    # 创建一个空的音频对象
    result = AudioSegment.empty()

    # 遍历每个切分的音频
    for chunk in chunks:
        # 随机生成一个无声时间的长度
        silent_time = random.randint(min_silent_time, max_silent_time)
        # 创建一个无声的音频对象
        silent_chunk = AudioSegment.silent(duration=silent_time)
        # 将无声的音频对象添加到切分的音频后面
        chunk += silent_chunk
        # 将拼接后的音频对象添加到结果中
        result += chunk

    # 保存结果为新的音频文件
    new_path = audio_path[0:-4]+"_sli"+".wav"
    
    print("new_path silence:",new_path)
    # 这里之后添加一个osremove
    result.export(new_path, format="wav")
    
    return new_path

import os

def wav_to_silk(out_wav, out_pcm, output_file):
    # 调用 ffmpeg 命令，将 wav 文件转换成 PCM raw data 文件
    add_silence_wav = add_silence(out_wav)
    subprocess.run(["C:\\Users\\蔡卓悦\\Documents\\Windows-quickstart-go-cqhttp-refs.tags.v2.5.1\\ffmpeg", "-i", add_silence_wav, "-ar", "24000", "-ac", "1", "-f", "s16le", out_pcm])
    # 调用 pilk 模块，将 PCM raw data 文件转换成 silk 文件
    pilk.encode(out_pcm, output_file, pcm_rate=24000, tencent=True)
    os.remove(out_wav)
    os.remove(out_pcm)
    print("hello !!!!!!!!!!!!!!!")
    return True

if __name__ == "__main__":
    wav_to_silk(sys.argv[1], sys.argv[2], sys.argv[3])