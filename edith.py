# coding:utf-8
import pyaudio
import wave
from baidu_speech_api import BaiduVoiceApi
import json
import signal
import sys
import RPi.GPIO as GPIO
import os
from aip.speech import AipSpeech
from regular import Regular_question
from play_music import music_list
from urllib2 import Request, urlopen, URLError, HTTPError


RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 1
RESPEAKER_WIDTH = 2
CHUNK = 1024
RECORD_SECONDS = 2
# WAVE_OUTPUT_FILENAME = "output.wav"

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.output(12, GPIO.LOW)
GPIO.output(13, GPIO.LOW)

p = pyaudio.PyAudio()
stream = p.open(
    rate=RESPEAKER_RATE,
    format=p.get_format_from_width(RESPEAKER_WIDTH),
    channels=RESPEAKER_CHANNELS,
    input=True,
    start=False,)

APP_ID = '16886339'
API_KEY = 'Ly0TST3N8Y7PA7pLrrou1PZX'
SECRET_KEY = 'O4BphHmbRrwL4K7jBIdHD9cuzVMWAKmg'


aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

baidu = BaiduVoiceApi(appkey=API_KEY, secretkey=SECRET_KEY)


def generator_list(list):
    for l in list:
        yield l


def record():
    stream.start_stream()
    print("* recording")
    frames = []
    for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("* done recording")
    stream.stop_stream()
    print("start to send to baidu")
    # audio_data should be raw_data
    text = baidu.server_api(generator_list(frames))
    if text:
        try:
            text = json.loads(text)
            for t in text['result']:
                print(t)
                return(t)
        except KeyError:
            return("get nothing")
    else:
        print("get nothing")
        return("get nothing")


def sigint_handler(signum, frame):
    stream.stop_stream()
    stream.close()
    p.terminate()
    print('catched interrupt signal!')
    sys.exit(0)


# 注册ctrl-c中断
signal.signal(signal.SIGINT, sigint_handler)

while True:
    try:
        outputtext = record()
        if (u'在吗') in outputtext:
            os.system("sudo mpg123 ./bgm/help.mp3")
            continue

        elif (u'吃饭了吗') in outputtext:
            os.system("sudo mpg123 ./bgm/eat.mp3")
            continue

        elif (u'名字') in outputtext:
            os.system("sudo mpg123 ./bgm/name.mp3")
            continue

        elif (u'天气') in outputtext:
            re = Regular_question()
            re.weather_now()
            continue

        elif (u'我回来了') in outputtext:
            os.system("sudo mpg123 ./bgm/home.mp3")
            continue

        elif (u'来啊') in outputtext:
            os.system("sudo mpg123 ./bgm/unknown.mp3")
            continue

        elif (u'几号') in outputtext:
            re = Regular_question()
            re.gettimeinfo(1)
            continue

        elif (u'几点') in outputtext:
            re = Regular_question()
            re.gettimeinfo(2)
            continue

        elif (u'放音乐') in outputtext:
            os.system("sudo mpg123 ./bgm/play_music.mp3")
            index = 0
            os.system("sudo mpg123 ./music/" + str(music_list(index)))
            continue

        elif (u'下一首') in outputtext:
            index += 1
            if index == 5:
                index = 0
            os.system("sudo mpg123 ./music/" + str(music_list(index)))
            continue

    except KeyError:
        stream.close()
        p.terminate()
