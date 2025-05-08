import cv2
import mediapipe as mp
import time


cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands            # create a hands object
hands = mpHands.Hands()                 # ( only works with RGB images)
mpDraw = mp.solutions.drawing_utils

prevTime = 0
currTime = 0

while True:
    success, img = cap.read()                       # read the image from the camera

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # convert the image to RGB

    results = hands.process(imgRGB)                 # process the image
    # print(results.multi_hand_landmarks)             

    if results.multi_hand_landmarks:
        for hand_i in results.multi_hand_landmarks:
            for id, lm in enumerate(hand_i.landmark):       # lm cho x,y coordinate
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                if id == 4:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            mpDraw.draw_landmarks(img, hand_i, mpHands.HAND_CONNECTIONS)

    currTime = time.time()
    fps = 1 / (currTime - prevTime)
    prevTime = currTime

# def putText(img: cv2.typing.MatLike, 
#               text: str, 
#               org: cv2.typing.Point, 
#               fontFace: int, 
#               fontScale: float, 
#               color: cv2.typing.Scalar, 
#               thickness: int = ..., 
#               lineType: int = ..., bottomLeftOrigin: bool = ...) -> cv2.typing.MatLike: ...

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (0, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
