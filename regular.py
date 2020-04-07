#coding:utf-8
#常规问题，如天气，日期，时间，星期

from aip.speech import AipSpeech
from weather import getWeatherStr
import os
import time

APP_ID = '16886339'
API_KEY = 'Ly0TST3N8Y7PA7pLrrou1PZX'
SECRET_KEY = 'O4BphHmbRrwL4K7jBIdHD9cuzVMWAKmg'

def str_to_mp3(string):
    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    result  = aipSpeech.synthesis(string, 'zh', 1, {
    'vol': 5, 'per': 5,})

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('./Music/regular.mp3', 'wb') as f:
            f.write(result)
        os.system("sudo mpg123 ./Music/regular.mp3")


class Regular_question:

    def weather_now(self):
        weather_str = getWeatherStr()
        str_to_mp3(weather_str)
        os.system("rm ./Music/regular.mp3")

    def gettimeinfo(self, kind):
        #1表示日期，2表示时间
        info = list(time.localtime())
        head = "现在是"
        if kind == 1:
            info_str = head + \
                str(info[0]) + "年" + \
                str(info[1]) + "月" + \
                str(info[2]) + "日" + \
                "星期" + str(info[6]+1)

        elif kind == 2:
            if info[3] >= 12:
                head_m = "下午"
                info[3] -= 12
            else:
                head_m = "上午"
            info_str = head + head_m + \
                str(info[3]) + "点" + \
                str(info[4]) + "分"

        str_to_mp3(info_str)
        os.system("rm ./Music/regular.mp3")
