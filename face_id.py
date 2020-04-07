from aip import AipFace
from picamera import PiCamera
import requests
import RPi.GPIO as GPIO
import base64
import time
import cv2
import os

F_APP_ID = '19259831'
F_API_KEY = 'dVbtljD3x2WW3dl3uEDfiBch'
F_SECRET_KEY = 'jXkueS42jlMiKiOKcR1KV4SqZ1lx4qnh'
client = AipFace(F_APP_ID, F_API_KEY, F_SECRET_KEY)

IMAGE_TYPE = 'BASE64'
GROUP = 'cde'

CMD_PATH = "sudo mpg123 ./Music/"

pic = PiCamera()

def getpic():
    pic.resolution = (1024, 768)
    pic.rotation = 180
    pic.start_preview()
    time.sleep(1)
    pic.capture('facepic.jpg')
    img = cv2.imread('facepic.jpg')
    cv2.imshow("FRAME", img)
    cv2.waitKey(2000)

def transpic():
    f = open('facepic.jpg', 'rb')
    img = base64.b64encode(f.read())
    return img

def go_baidu(pic):
    result = client.search(str(pic), IMAGE_TYPE, GROUP)
    if result['error_msg'] == 'SUCCESS':
        name = result['result']['user_list'][0]['user_id']
        score = result['result']['user_list'][0]['score']
        if score > 80:
            if name == 'cde':
                os.system("sudo mpg123 ./Music/cde.mp3")
                time.sleep(3)
            elif name == 'min':
                os.system("sudo mpg123 ./Music/min.mp3")
                time.sleep(3)   
            elif name == 'ran':
                os.system("sudo mpg123 ./Music/ran.mp3")
                time.sleep(3)          
        else:
            os.system("sudo mpg123 ./Music/unknown.mp3")
            name = 'Unknow'
            return 0
            
        current_time = time.asctime(time.localtime(time.time()))

        f = open('Log.txt', 'a')
        f.write("Person:" + name + "  " + "Time:" + str(current_time) + '\n')
        f.close()
        return 1

    if result['error_msg'] == 'pic not has face':
        os.system(CMD_PATH + "noface.mp3")
        time.sleep(2)
        return 0
    else:
        print(str(result['error_code']) + '-' + result['error_msg'])
        return 0

if __name__ == '__main__':
    print("ready!go")
        
    getpic()
    pic = transpic()
    res = go_baidu(pic)
    if res == 1:
        print("welcome")
    else:
        print("???")
    os.system("rm ./Pic/facepic.jpg")
