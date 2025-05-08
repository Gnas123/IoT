import cv2
import mediapipe as mp
import time

# ref https://chuoling.github.io/mediapipe/solutions/hands.html


class handDetector():
    def __init__(self, 
                static_image_mode=False,
                max_num_hands=2,
                model_complexity=1,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.model_complexity = model_complexity
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpHands = mp.solutions.hands            # create a hands object
        # ( only works with RGB images)
        self.hands = self.mpHands.Hands(self.static_image_mode, 
                                        self.max_num_hands, 
                                        self.model_complexity,
                                        self.min_detection_confidence, 
                                        self.min_tracking_confidence)               
        self.mpDraw = mp.solutions.drawing_utils     # draw the landmarks


    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   # convert the image to RGB

        self.results = self.hands.process(imgRGB)                 # process the image
        # print(results.multi_hand_landmarks)             

        if self.results.multi_hand_landmarks:
            for hand_i in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, hand_i, self.mpHands.HAND_CONNECTIONS)
                else:
                    print("No hands detected")
                
    
        return img
 
    def findPosition(self, img, handNo=0, draw=True, pos=[]):
        lmList = []
        if self.results.multi_hand_landmarks:
            hand_i=self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(hand_i.landmark):       # lm cho x,y coordinate
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    if id in pos:    
                        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
                        
        return lmList


# def main():
#     prevTime = 0
#     currTime = 0
    
#     cap = cv2.VideoCapture(0)

#     detector = handDetector()

#     while True:
#         success, img = cap.read()                       # read the image from the camera
#         img = detector.findHands(img, success)

#         lmList = detector.findPosition(img)
#         if len(lmList) != 0:
#             print(lmList[4])
#             print(lmList[8])
            



#         currTime = time.time()
#         fps = 1 / (currTime - prevTime)
#         prevTime = currTime

# # def putText(img: cv2.typing.MatLike, 
# #               text: str, 
# #               org: cv2.typing.Point, 
# #               fontFace: int, 
# #               fontScale: float, 
# #               color: cv2.typing.Scalar, 
# #               thickness: int = ..., 
# #               lineType: int = ..., bottomLeftOrigin: bool = ...) -> cv2.typing.MatLike: ...

#         cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
#                     (0, 0, 255), 2)

#         cv2.imshow("Image", img)
#         cv2.waitKey(1)


# if __name__ == "__main__":
#     main()