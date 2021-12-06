import os
import time

import cv2
import pyttsx3

import HandTrackingModule as hTm

wCam, hCam = 740, 580
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
folderPath = "FingerImages"
numberList = os.listdir(folderPath)
folder_gesture = 'FingerGesture'
gestureList = os.listdir(folder_gesture)
print(numberList)
overlayList = []
for imPath in numberList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
gestures = []
for imPath in gestureList:
    image = cv2.imread(f'{folder_gesture}/{imPath}')
    gestures.append(image)
print(len(overlayList))
pTime = 0
detector = hTm.HandDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]
previousNumber = None
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    engine = pyttsx3.init()

    # imageRun = threading.Thread(target=findNumbersUp(lmList))
    # imageRun.start()
    # # soundRun = threading.Thread(target=loadSound())
    # # soundRun.start()
    # # soundRun.join()
    # imageRun.join
    if len(lmList) != 0:
        if lmList[4][1] < lmList[20][1]:
            sided = "left"
        else:
            sided = "right"
        fingers = []
        if sided == 'right':
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        # 4 Fingers
        for ImgId in range(1, 5):
            if lmList[tipIds[ImgId]][2] < lmList[tipIds[ImgId] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)
        # if totalFingers == 2 and fingers[0] == 1 and fingers[4] == 1:
        #     h, w, c = gestures[0].shape
        #     img[0:h, 0:w] = gestures[0]
        #     cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        #     cv2.putText(img, "+", (45, 375), cv2.FONT_HERSHEY_PLAIN,
        #                 10, (255, 0, 0), 25)
        # elif totalFingers == 1 and fingers[2] == 1:
        #     h, w, c = gestures[0].shape
        #     img[0:h, 0:w] = gestures[0]
        #     cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        #     cv2.putText(img, "Avoid these Gestures!", (45, 375), cv2.FONT_HERSHEY_PLAIN,
        #                 1, (255, 0, 0), 2)
        # else:
        h, w, c = overlayList[totalFingers - 1].shape
        img[0:h, 0:w] = overlayList[totalFingers - 1]
        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)
        if totalFingers != previousNumber:
            engine.say(str(totalFingers))
            engine.runAndWait()
            del engine
            previousNumber = totalFingers

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
