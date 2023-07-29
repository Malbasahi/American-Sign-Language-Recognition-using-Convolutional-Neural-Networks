#loading important libraries 
import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math

#capturing video 
cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
#the path to the pre-trained model file
classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")

#resizing and cropping images 
offset = 20
imgSize = 300
 
#mapping the predictions to their corresponding alphabet labels 
folder = "Data/C"
counter = 0
 
labels = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", 
"M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
 
#captures a video stream frame by frame 
while True:
    success, img = cap.read()
    #makes a copy of the original frame to draw the bounding box and label the recognized gesture.
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']
        #blank image used to draw the resized cropped hand image
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255 
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
 
        imgCropShape = imgCrop.shape
 
        aspectRatio = h / w
 
        if aspectRatio > 1:
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = math.ceil((imgSize - wCal) / 2)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
            print(prediction, index)
 
        else:
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = math.ceil((imgSize - hCal) / 2)
            imgWhite[hGap:hCal + hGap, :] = imgResize
            prediction, index = classifier.getPrediction(imgWhite, draw=False)
 
        cv2.rectangle(imgOutput, (x - offset, y - offset-50),
                      (x - offset+90, y - offset-50+50), (255, 0, 255), cv2.FILLED)
        cv2.putText(imgOutput, labels[index], (x, y -26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
        cv2.rectangle(imgOutput, (x-offset, y-offset),
                      (x + w+offset, y + h+offset), (255, 0, 255), 4)
 
 
        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)
 
    cv2.imshow("Image", imgOutput)
    cv2.waitKey(1) 