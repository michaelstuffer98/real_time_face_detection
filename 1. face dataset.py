''''
Capture multiple Faces from multiple users to be stored on a DataBase (dataset directory)
	==> Faces will be stored on a directory: dataset/ (if does not exist, pls create one)
	==> Each face will have a unique numeric integer ID as 1, 2, 3, etc
'''

from time import sleep
import cv2
import os
from config_loader import ConfigLoader
import re

# For each person, enter one numeric face id (must enter number start from 1, this is the lable of person 1)
face_id = ""
while len(face_id) == 0:
    face_id = input('\n==> enter user id end press <return> :  ')
    if any( [ re.search("User." + face_id + ".[0-9]+.jpg", f) for f in os.listdir('dataset/') ] ):
        print("[WARNING] User name already exists in data base, continuing will overwrite existing files")
        k = input("Continue? [y|n]\t").lower()
        if k == "y":
            break
        elif k == "n":
            face_id = ""
            continue

#start detect your face and takes n pictures
config = ConfigLoader()
n_pictures = config["pictures_per_person"]
capture_interval = config["capture_interval"]

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height

#make sure 'haarcascade_frontalface_default.xml' is in the same folder as this code
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = 0
failed = 0

while(count < n_pictures):

    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        failed += 1
        if failed % 5 == 0:
            failed = 0
            print("[WARNING] Can't detect your face!")
    
    sleep(capture_interval)

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1
        failed = 0
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
        # cv2.imshow('image', img)
        print("\t", count/n_pictures * 100.0, " %", end='\r')

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        print("[ERROR] Abort process, cleaning up...")
        cam.release()
        cv2.destroyAllWindows()
        [ os.remove(file) for file in os.listdir('dataset/') if re.search("User." + face_id + ".[0-9]+.jpg", file) ]
        raise RuntimeError("Process cancelled by User")

print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()