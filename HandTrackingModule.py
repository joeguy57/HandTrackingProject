"""
This a module that uses the images being sent through to identify the number being shown above.
"""
import cv2
import mediapipe as mp
import time


class HandDetector:
    """
    This class helps find hands that display on the screen
    """
    def __init__(self, mode=False, maxHands=1, detectionCon=0.5, trackCon=0.5):
        """
        Initiates the hand detector.
        :param mode: Set to False throughout
        :param maxHands: The number of hands that can be detected
        :param detectionCon: The strength of the detection
        :param trackCon: the precision of tracking
        """
        self.results = None
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, 1, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        """
        Finds where the hands are in a screen and identifies each joint.
        :param img: the input of the webcam
        :param draw: the indication for each index
        :return: the manipulated image
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        """
        Returns the coordinates of each landmark on the hand
        :param img: the input of the webcam
        :param handNo: the number on the hand
        :param draw: the indexes being drawn on
        :return: a List of the positions
        """
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for ImgId, lm in enumerate(myHand.landmark):
                # print(ImgId, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(ImgId, cx, cy)
                lmList.append([ImgId, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmList

#
# def main():
#     """
#     Runs the class in order to process the hands.
#     :return:
#     """
#     pTime = 0
#     cap = cv2.VideoCapture(1)
#     detector = HandDetector()
#     while True:
#         success, img = cap.read()
#         img = detector.findHands(img)
#         lmList = detector.findPosition(img)
#         if len(lmList) != 0:
#             print(lmList[4])
#         cTime = time.time()
#         fps = 1 / (cTime - pTime)
#         pTime = cTime
#         cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
#                     (255, 0, 255), 3)
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)
#
#
# if __name__ == "__main__":
#     main()
