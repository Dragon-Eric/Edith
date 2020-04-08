#coding:utf-8

from aip.speech import AipSpeech
import os

APP_ID = '16886339'
API_KEY = 'Ly0TST3N8Y7PA7pLrrou1PZX'
SECRET_KEY = 'O4BphHmbRrwL4K7jBIdHD9cuzVMWAKmg'

def generate_mp3(str, name):
    #str 传入的语句
    #name 保存后的文件名

    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    result  = aipSpeech.synthesis(str, 'zh', 1, {
        'vol': 5, 'per': 5,
    })

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        filename = './bgm/' + 'name' + '.mp3'
        with open(filename, 'wb') as f:
            f.write(result)

