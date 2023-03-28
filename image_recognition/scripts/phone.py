import requests as req
import recognize as recog
import camera
import pygame
import sys

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
            newItems = recog.recognize(imageName)
            print(newItems)
