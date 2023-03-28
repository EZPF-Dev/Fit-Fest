# Python program to capture a single image
# using pygame library
  
# importing the pygame library
import pygame
import pygame.camera
import sys
import keyboard

def initialize_photo ():
 # initializing  the camera
 pygame.camera.init()
  
 # make the list of all available cameras
 camlist = pygame.camera.list_cameras()
  
 # if camera is detected or not
 if camlist:
  
    # initializing the cam variable with default camera
    cam = pygame.camera.Camera(camlist[0], (640, 480))
  
    # opening the camera
    cam.start()
 else:
    print("Not camera detected")
    
    
 return cam

def take_photo(cam):  
    # capturing the single image
    image = cam.get_image()
  
    # saving the image
    imagePath = "/home/fitfest/Desktop/Fit-Fest/image_recognition/images/filename.bmp"
    pygame.image.save(image, imagePath)
    return imagePath
    # pygame.camera.Camera.stop()

def camera_off (cam):
   cam.stop()