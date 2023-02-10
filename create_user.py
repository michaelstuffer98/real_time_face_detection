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
import utils
from profiles import *

# For each person, enter one numeric face id (must enter number start from 1, this is the lable of person 1)
VISUALIZE = False

def abort(cam, face_id: str, profiles: Profiles):
    print("[ERROR] Abort process, cleaning up...")
    cam.release()
    cv2.destroyAllWindows()
    profiles.remove_profile(face_id)
    print("Process cancelled by User")
    exit(1)

face_id = ""
profiles = Profiles()

while 1:
    face_id = input('\n==> enter user id end press <return> :  ')
    if len(face_id) == 0:
        continue
    ret = profiles.add_profile(face_id)
    print(ret[1])

    if ret[0] == PROFILE_RET.OK:
        break

    if ret[0] == PROFILE_RET.DUPLICATE:
        print("[WARNING] User name already exists in data base, continuing will delete existing user pictures")
        k = ""
        while(not k in ['n', 'y']):
            k = input("Continue? [y|n]\t").lower()
        if k == "y":
            [ os.remove('dataset/' + file) for file in os.listdir('dataset/') if re.search("User." + face_id + ".[0-9]+.jpg", file) ]
            break
        elif k == "n":
            face_id = ""
            continue
    elif ret[0] == PROFILE_RET.FAILURE:
        exit(1)

#start detect your face and takes n pictures
config = ConfigLoader()
n_pictures = config["pictures_per_person"]
capture_interval = config["capture_interval"]

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
width = 640
height = 480
cam.set(3, width) # set video width
cam.set(4, height) # set video height

#make sure 'haarcascade_frontalface_default.xml' is in the same folder as this code
face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

print("\n [INFO] Initializing face capture. Look the camera and wait ...")
# Initialize individual sampling face count
count = 0
failed = 0
# Pad pixels at each side
padding = 15
try:
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

        for face in faces:
            (x, y, w, h) = face# utils.pad(face, padding, width, height)
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            count += 1
            failed = 0
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            
            if VISUALIZE:
                cv2.imshow('image', img)
            
            utils.print_progress(count/n_pictures)

        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            abort(cam, face_id, profiles)
except KeyboardInterrupt as e:
    abort(cam, face_id, profiles)



print("\n [INFO] Done, created profile for ", face_id, " (", n_pictures, " pictures taken)")
cam.release()
cv2.destroyAllWindows()