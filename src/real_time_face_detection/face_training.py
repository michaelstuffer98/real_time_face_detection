''''
Training Multiple Faces stored on a DataBase:
	==> Each face should have a unique numeric integer ID as 1, 2, 3, etc                       
	==> LBPH computed model will be saved on trainer/ directory. (if it does not exist, pls create one)
	==> for using PIL, install pillow library with "pip install pillow"

Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18   

'''

import cv2
import numpy as np
from PIL import Image #pillow package
import os
import real_time_face_detection.utils as utils
from real_time_face_detection.profiles import Profiles


# function to get the images and label data
def getImagesAndLabels(path, detector):
    # Set up a generator to iterate through the image directory
    image_dir = utils.image_dir_generator(path)
    # image_dir = [ os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    faceSamples=[]
    ids = []
    # n_images = len(image_dir)
    
    profiles = Profiles()
    static_id = 1
    blacklist = []

    for imagePath in image_dir:
        PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
        img_numpy = np.array(PIL_img,'uint8')

        name = os.path.split(imagePath)[-1].split(".")[1]
        if name in blacklist:
            continue
        try:
            id = int(profiles.profiles[name])
            if id == 0:
                id = profiles.profiles[name] = static_id
                static_id += 1 
        except KeyError:
            blacklist.append(name)
            print("picture face_id '" + name + "' is not registered in profile data base, skipping")
            continue

        faces = detector.detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            faceSamples.append(img_numpy[y:y+h,x:x+w])
            ids.append(id)

        # utils.print_progress(i/n_images)
    profiles.flush()

    return faceSamples,ids


def main():
    # Path for face image database
    path = 'dataset'

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    print ("\n [INFO] Training face models")
    faces,ids = getImagesAndLabels(path, detector)
    recognizer.train(faces, np.array(ids))

    # Save the model into trainer/trainer.yml
    recognizer.write('model/trainer.yml')



    # Print the numer of faces trained and end program
    print("\n [INFO] Finished: {0} faces trained.".format(len(np.unique(ids))))
