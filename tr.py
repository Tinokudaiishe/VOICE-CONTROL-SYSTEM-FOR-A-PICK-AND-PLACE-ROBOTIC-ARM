import cv2
import numpy as np
import math
import time
import json
import serial
import time
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO
import serial

import speech_recognition as sr
searchCount =0
# Create a Recognizer object
r = sr.Recognizer()

# Use the default microphone as the audio source
import speech_recognition as sr
import os
import playsound
from google.cloud import texttospeech
import os
import pygame
import os
takeWater= False
# Initialize Pygame mixer
pygame.mixer.init()

import os

# Load and play the audio file


sound = pygame.mixer.Sound("wel.mp3")
sound.play()

# Wait for the audio to finish playing
while pygame.mixer.get_busy():
    continue

import time
time.sleep(3)
# Initialize Pygame mixer
pygame.mixer.init()
# Load and play the audio file
sound = pygame.mixer.Sound("myname.mp3")
sound.play()

# Wait for the audio to finish playing
while pygame.mixer.get_busy():
    continue

sound = pygame.mixer.Sound("intro.mp3")
sound.play()

# Wait for the audio to finish playing
while pygame.mixer.get_busy():
    continue
def listenToPerson():
    takeWater =False
    while True:
        with sr.Microphone() as source:
            print("Speak something...")
            audio = r.listen(source, timeout=5)

        try:
            text = r.recognize_google(audio)
            print("You said:", text)

            # Check if the word "banana" is found in the spoken text
            if "octopus" in text.lower():
                print("Initialized!")   
                # Play an audio file
                # Load and play the audio file
                sound = pygame.mixer.Sound("get.mp3")
                sound.play()
                # Wait for the audio to finish playing
                #
                while pygame.mixer.get_busy():
                    continue
                break
            elif "water bottle" in text.lower():
                print("Initialized!")   
                # Play an audio file
                # Load and play the audio file
                sound = pygame.mixer.Sound("getwater.mp3")
                sound.play()
                # Wait for the audio to finish playing
                #
                while pygame.mixer.get_busy():
                    continue
                takeWater= True
                break

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return takeWater

while True:
    water= listenToPerson()
    if water:
        print("Now commanding arm")
        break
print("Wheel chair assistant")
# Open the webcam
#Z
# Check if the webcam is opened successfully
cap = cv2.VideoCapture(1)

def findCenter(x1, x2,y1, y2):
    xc= ((x2-x1)/2)+x1
    yc= ((y2-y1)/2)+y1
    return xc, yc 

import json
def makePrediction(img):
    model = YOLO('yolov8n.pt')
    results = model.predict(img, stream=True, imgsz= 480, conf=0.5)                 # run prediction on img
    cv2.imshow('DETECTION', img)
    value=9
    cv2.waitKey(1)
    got=0
    for result in results:
        boxes = result.boxes.cpu().numpy()
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0].astype(int)
            label = f"{x1}, {y1}, {x2}, {y2}"
            cl = int(box.cls[0])
            print(f"The class is:  {cl}")
            if cl == 39:
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(img, "WATER BOOTLE DETECTED", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                centerX, centerY= findCenter(x1, x2,y1, y2)
                searchCount=0
                got=1
                xmid =int(centerX)
                ymid= int(centerY)
                height, width, channels = img.shape
                # Calculate the center coordinates
                center_x = width // 2
                center_y = height // 2
                print(f"X value: {centerX}, Y value: {centerY} ")
                cv2.putText(img, f"({xmid}, {ymid}) CENTER", (xmid-10, ymid- 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(img, f"({center_x}, {center_y})  IMG CENTER", (center_x-30, center_y- 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                error_x = center_x-xmid     
                cv2.putText(img, f"ERROR X VALUE: {error_x}", (50, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2) 
                if error_x > 40:
                    print("Move left ")  
                    value=1
                elif error_x <=40 and error_x > -40:
                    print("Move gripper foward!!")
                    value=3
                elif error_x<=-40:
                    print("Move right ") 
                    value=2
            else:
                print(" No human detected !! !!!")
            cv2.imshow('DETECTION', img)
            cv2.waitKey(1)
        return got, value

def sendCommand(base):
    try:
        with serial.Serial('COM15', 9600, timeout=1) as ser:
            # Convert the integer to a byte string
            value_bytes = str(base).encode()
            
            # Write the byte string to the serial port
            ser.write(value_bytes)
            print(f"Sent value: {value_bytes}") 
    except serial.SerialException as e:
        print(f"Serial communication error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
if not cap.isOpened():
    print("Failed to open the webcam")
    exit()

while True:                                         
    # Read a frame from the webcam
    ret, frame = cap.read() 
    found, value= makePrediction(frame)
    if found>0:
         searchCount=0
         sendCommand(value)
    if searchCount<15:
         if value!=10:
             if found<=0:
                 sendCommand(1)
         searchCount =searchCount+1
         print(f"Search count is {searchCount}")
    else:
        no_detection=True
        sendCommand(8)
        sound = pygame.mixer.Sound("outofsight.mp3")
        sound.play()
    
        while pygame.mixer.get_busy():
            continue

        while True:
            pass
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
