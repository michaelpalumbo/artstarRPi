# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
import websocket
import getmac
import socket
import subprocess

hostname = socket.gethostname()
ip = subprocess.getoutput("hostname -I")
try:
    import thread
except ImportError:
    import _thread as thread
    
mac = getmac.get_mac_address()



"""Small example OSC client

This program sends 10 random values between 0.0 and 1.0 to the /filter address,
waiting for 1 seconds between each value.
"""
import argparse
import random
import time

from pythonosc import udp_client


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip", default="192.168.0.102",
      help="The ip of the OSC server")
  parser.add_argument("--port", type=int, default=5005,
      help="The port the OSC server is listening on")
  args = parser.parse_args()

  client = udp_client.SimpleUDPClient(args.ip, args.port)
  print('udpClient', args)
  register = mac + '_' + hostname + '_' + ip
  client.send_message('trackerReg', register)

#  for x in range(10):
#    client.send_message("/filter", random.random())
#    time.sleep(1)

# provide path to the haar cascade at python livecam.py
#cascPath = sys.argv[1]
cascPath = './haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    
    client.send_message(mac, len(faces))
    #len(faces)
    print(mac)
    # Draw a rectangle around the faces
    #for (x, y, w, h) in faces:
        #cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
        
        #print('dims', faces)
    
    #cv2.imshow('Video', image)    
    rawCapture.truncate(0)
#    rawCapture.seek(0)
#    if process(rawCapture):
#        break

    #if cv2.waitKey(1) & 0xFF == ord('q'):
        #break

    # show the frame
    #cv2.imshow("Frame", gray)
    #key = cv2.waitKey(1) & 0xFF
 
     #is this where the cv happens?
 
 
    # clear the stream in preparation for the next frame
    #rawCapture.truncate(0)
 
    # if the `q` key was pressed, break from the loop
    #if key == ord("q"):
     #   break
     

