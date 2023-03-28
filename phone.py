import requests as req
import recognize as recog

key_pressed = False

while(True):
    if key_pressed:
        picture = takePicture()
        items = recog.recognize(picture)
        print(items)