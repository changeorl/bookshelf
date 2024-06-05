options = [
    "zh-CN-XiaoxiaoNeural",
    "zh-CN-XiaoyiNeural",
    "zh-CN-YunjianNeural",
    "zh-CN-YunxiNeural",
    "zh-CN-YunxiaNeural",
    "zh-CN-YunyangNeural",
    "zh-CN-liaoning-XiaobeiNeural",
    "zh-CN-shaanxi-XiaoniNeural",
    "zh-HK-HiuGaaiNeural",
    "zh-HK-HiuMaanNeural",
    "zh-HK-WanLungNeural",
    "zh-TW-HsiaoChenNeural",
    "zh-TW-HsiaoYuNeural",
    "zh-TW-YunJheNeural",
]

text = """那是一九二三年夏天的事了。那年夏天，我不顾姑妈要我返回什罗普郡的期望，离开剑桥南下，决定未来在首都发展，于是租下肯辛顿区贝德福德花园街十四号b室这间小公寓。"""

import os
for voice in options:
    media = f"audio/{voice}.mp3"

    command = f'edge-tts --text "{text}" --voice {voice} --write-media {media}'
    os.system(command)

    print(f"FINISHED! {command}")