import requests as req
import recognize as recog
import camera
import pygame
import sys
import json
import requests

url = 'http://192.168.88.165:5000/ingredients'

pygame.init()

 # creating display
display = pygame.display.set_mode((5, 5))

def takePhoto():
    cam = camera.initialize_photo()
    imageName = camera.take_photo(cam)
    camera.camera_off(cam)
    
    return imageName

 # creating a running loop
while True:    
    # creating a loop to check events that
    # are occurring
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         
        # checking if keydown event happened or not
        if event.type == pygame.KEYDOWN:
           
            # if keydown event happened
            # than printing a string to output
            print("A key has been pressed")
            imageName = takePhoto()
            print('here')
            newItems = recog.recognize(imageName)
            ingredients = {'ingredients':newItems}
            myobj = json.dumps(ingredients)
            objstring= json.loads(myobj)
            myobj2=json.dumps(objstring)
            print (objstring['ingredients'])
            print(myobj2)

            x = requests.post(url, json = myobj2) 
            

            
