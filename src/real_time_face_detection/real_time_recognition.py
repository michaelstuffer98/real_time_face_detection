''''
Real Time Face Recogition
	==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model (trained faces) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18  

'''

from configparser import ConfigParser
import cv2
import numpy as np
import os
from src.config_loader import ConfigLoader 
from src.profiles import Profiles
import numpy as np
from collections import deque as dq

class FaceAveraging:
    def __init__(self, avg_frames: int) -> None:
        self.N = avg_frames
        self.faces = {}
        self.kernel = np.ones(self.N)/self.N

    def new_frame(self, x, y, w, h, id):
        if id == "unknown":
            return (x, y, w, h)
        if id not in self.faces:
            self.faces[id] = (dq([x], self.N), dq([y], self.N), dq([w], self.N), dq([h], self.N))
        else:
            self.faces[id][0].append(x)
            self.faces[id][1].append(y)
            self.faces[id][2].append(w)
            self.faces[id][3].append(h)
        f = self.faces[id]
        return (int(np.mean(f[0])), int(np.mean(f[1])), int(np.mean(f[2])), int(np.mean(f[3])))


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('model/trainer.yml')   #load trained model
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter, the number of persons you want to include

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

profiles = Profiles()

config = ConfigLoader()
faces_avg = FaceAveraging(config.get("frame_averaging"))

while True:

    ret, img =cam.read()

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )

    for(x,y,w,h) in faces:
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 100):
            found = False
            for k, v in profiles.profiles.items():
                if v == id:
                    found = True
                    id = k
            if not found:
                id = "label " + str(id)
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        (x, y, w, h) = faces_avg.new_frame(x, y, w, h, id)

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
