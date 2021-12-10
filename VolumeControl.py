"""
This file initiates our module and begins the process of
identifying fingers that are placed up, to see manipulate devices volume:
1 finger:
    - going up increases volume by two
    - going down decreases volume by two
2 fingers:
    - sets the volume (must be held until fingers are off-screen)
5 fingers:
    - Increases to full volume must be held until volume reaches 100%
0 fingers:
    - Mutes device
"""
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import cv2
import pyautogui
import pyttsx3

import HandTrackingModule as hTm

wCam, hCam = 740, 580
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detector = hTm.HandDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]
totalFingers = None
previous_index_position = None
volumeSet = False
volumeMute = True
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    engine = pyttsx3.init()
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
        if previous_index_position is not None:
            if lmList[8][2] < previous_index_position:
                if not volumeSet:
                    print("Volume is increasing")
                    for i in range(2):
                        pyautogui.press("volumeup")
                # print(lmList[8][2])
                # print(previous_index_position)
            elif lmList[8][2] > previous_index_position:
                if not volumeSet:
                    print("Volume is decreasing")
                    for i in range(2):
                        pyautogui.press("volumedown")
            if totalFingers == 2:
                volumeMute = True
                volumeSet = True
                print("The volume is set")
            elif totalFingers == 1:
                print("Volume reverted to basic")
                volumeSet = False
            elif totalFingers == 0:
                if volumeMute:
                    print("volume is mute")
                    volumeSet = True
                    volumeMute = False
                    pyautogui.press('volumemute')
            elif totalFingers == 5:
                print("volume is full")
                maxVolume = 0.0
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                currentVolume = volume.GetMasterVolumeLevel()
                volume.SetMasterVolumeLevel(maxVolume, None)
                volumeSet = True
                pyautogui.keyDown("volumeup")
        previous_index_position = lmList[8][2]
        totalFingers = fingers.count(1)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
