# phan mem chinh de kieu khien quat bang tay
import cv2
import numpy as np
import time
from .mediapipeModule import *
import math

thread_number = 0

def get_thread_number():
    return thread_number

def send_data_quat(client, scaled_value):
    # Simulated function to send data (replace with your actual sending logic)
    print(f"Sending scaled value: {scaled_value}")
    client.publish("data-quat", scaled_value)  # Publish the scaled value to the MQTT topic

# Simulated function to send signals (replace with your actual signal-sending logic)
def send_signal(action):
    print(f"Sending signal: {action}")
    return scaled_value

def start_camera(client_arg, is_on=True):
    global thread_number
    thread_number += 1

    prevTime = 0
    currTime = 0
    last_signal_time = 0  # To track the last time a signal was sent
    last_signal_time_data = 0  # To track the last time a signal was sent
    debounce_delay = 0.5  # Minimum time (in seconds) between signals
    # is_on = False  # State tracking: False = off, True = on

    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()  # Read the image from the camera
        if not success or img is None:
            print("Failed to capture image from camera.")
            break


        detector.findHands(img, success)
        lmList = detector.findPosition(img, draw=True, pos=[4, 8])  # Thumb (4) and Index (8)

        # Draw line and calculate length
        if len(lmList) >= 8:
            x1, y1 = lmList[4][1], lmList[4][2]  # Thumb tip
            x2, y2 = lmList[8][1], lmList[8][2]  # Index tip
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # length between finger
            # ? 50 <= line_length <= 200
            line_length = math.hypot(x2 - x1, y2 - y1)
            # print("line_length: ", line_length)

            # scale to volume from 0 to 100
            scaled_value = np.interp(line_length, [50, 150], [0, 100])
            # Ensure value is within bounds
            scaled_value = round(np.clip(scaled_value, 0, 100))


            # *adafruite part------------------------------------------------
            
            curr_time = time.time()
            #! 3s moi gui data, tranh bi banned :<
            if is_on and ((curr_time - last_signal_time_data) > 3):
                send_data_quat(client_arg, scaled_value)
                last_signal_time_data = curr_time

            # *adafruite part------------------------------------------------



            # print(line_length)

            # Midpoint circle
            mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.circle(img, (mid_x, mid_y), 15, (255, 0, 255), cv2.FILLED)

            #! Check finger distance and send signal with debounce and state tracking
            # curr_time = time.time()
            # if line_length < 50:
            #     #* Green when close
            #     cv2.circle(img, (mid_x, mid_y), 15, (0, 255, 0), cv2.FILLED)  
            #     if (curr_time - last_signal_time) > debounce_delay:  # Debounce check / time between each signals
            #         # case dang bat
            #         if is_on: 
            #             is_on = False
            #             client_arg.publish("nut-quat", "OFF")
            #             print("nut-quat: ", "OFF")
            #             last_signal_time = curr_time
            #         # case dang tat
            #         else:
            #             is_on = True
            #             client_arg.publish("nut-quat", "ON")
            #             print("nut-quat: ", "ON")
            #             last_signal_time = curr_time

        # Calculate and display FPS
        currTime = time.time()
        fps = 1 / (currTime - prevTime) if (currTime - prevTime) > 0 else 0
        prevTime = currTime

        # * 1 so thong tin hien thi tren cam
        cv2.putText(img, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)

        cv2.imshow("Image", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit on 'q' key
            client_arg.publish("nut-quat", "OFF")
            break
        if cv2.waitKey(1) & 0xFF == 27:  # Exit on 'ESC' key
            client_arg.publish("nut-quat", "OFF")
            break

    cap.release()
    cv2.destroyAllWindows()

    thread_number -= 1
    print("Camera stopped...")



# if __name__ == "__main__":
#     start_camera()